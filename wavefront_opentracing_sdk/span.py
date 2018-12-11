"""
Wavefront Span.

@author: Hao Song (songhao@vmware.com)
"""
import threading
import time
from opentracing import Span
from wavefront_sdk.common.utils import is_blank


# pylint: disable=too-many-instance-attributes
class WavefrontSpan(Span):
    """Wavefront Span."""

    # pylint: disable=too-many-arguments
    def __init__(self, tracer, operation_name, context, start_time, parents,
                 follows, tags):
        """
        Construct Wavefront Span.

        :param tracer: Tracer that create this span
        :type tracer: wavefront_opentracing_python_sdk.WavefrontTracer
        :param operation_name: Operation Name
        :type operation_name: str
        :param context: Span Context
        :type context: wavefront_opentracing_python_sdk.WavefrontSpanContext
        :param start_time: an explicit Span start time as a unix timestamp per
            :meth:`time.time()`
        :type start_time: float
        :param parents: List of UUIDs of parents span
        :type parents: list of uuid.UUID
        :param follows: List of UUIDs of follows span
        :type follows: list of uuid.UUID
        :param tags:
        """
        super(WavefrontSpan, self).__init__(tracer=tracer, context=context)
        self._context = context
        self.operation_name = operation_name
        self.start_time = start_time
        self.duration_time = 0
        self.parents = parents
        self.follows = follows
        self.tags = tags
        self._finished = False
        self.update_lock = threading.Lock()

    @property
    def context(self):
        """Get WavefrontSpanContext of WavefrontSpan.

        :return: Span context of current span.
        :rtype: wavefront_opentracing_python_sdk.WavefrontSpanContext
        """
        return self._context

    def set_tag(self, key, value):
        """
        Set tag of span.

        :param key: key of the tag
        :type key: str
        :param value: value of the tag
        :type value: str
        :return: span itself
        :rtype: WavefrontSpan
        """
        with self.update_lock:
            if not is_blank(key) and value:
                self.tags.append((key, value))
        return self

    def set_baggage_item(self, key, value):
        """
        Replace span context with the updated dict of baggage.

        :param key: key of the baggage item
        :type key: str
        :param value: value of the baggage item
        :type value: str
        :return: span itself
        :rtype: WavefrontSpan
        """
        new_context = self._context.with_baggage_item(key=key, value=value)
        with self.update_lock:
            self._context = new_context
        return self

    def get_baggage_item(self, key):
        """
        Get baggage item with given key.

        :param key: Key of baggage item
        :type key: str
        :return: Baggage item value
        :rtype: str
        """
        return self._context.get_baggage_item(key)

    def set_operation_name(self, operation_name):
        """
        Update operation name.

        :param operation_name: Operation Name
        :type operation_name: str
        :return: Span itself
        :rtype: WavefrontSpan
        """
        with self.update_lock:
            self.operation_name = operation_name
        return self

    def finish(self, finish_time=None):
        """
        Call finish to finish current span, and report it.

        :param finish_time: Finish time, unix timestamp
        :type finish_time: float
        """
        if finish_time:
            self._do_finish(finish_time - self.start_time)
        else:
            self._do_finish(time.time() - self.start_time)

    def _do_finish(self, duration_time):
        """
        Mark span as finished and send it via reporter.

        :param duration_time: Duration time in seconds
        :type duration_time: float
        """
        with self.update_lock:
            if self._finished:
                return
            self.duration_time = duration_time
            self._finished = True
        self.tracer.report_span(self)

    @property
    def trace_id(self):
        """
        Get trace id.

        :return: Trace id
        :rtype: uuid.UUID
        """
        return self._context.trace_id

    @property
    def span_id(self):
        """
        Get span id.

        :return: Span id
        :rtype: uuid.UUID
        """
        return self._context.span_id

    def get_operation_name(self):
        """
        Get operation name.

        :return: Operation name.
        :rtype: str
        """
        return self.operation_name

    def get_start_time(self):
        """
        Get span start time.

        :return: Span start time, unix timestamp.
        :rtype: float
        """
        return self.start_time

    def get_duration_time(self):
        """
        Get span duration time.

        :return: Span duration time in seconds.
        :rtype: float
        """
        return self.duration_time

    def get_parents(self):
        """
        Get list of parents span's id.

        :return: list of parents span's id
        :rtype: list of uuid.UUID
        """
        if not self.parents:
            return []
        return self.parents

    def get_follows(self):
        """
        Get list of follows span's id.

        :return: list of follows span's id
        :rtype: list of uuid.UUID
        """
        if not self.follows:
            return []
        return self.follows

    def get_tags(self):
        """
        Get tags of span.

        :return: list of tags
        :rtype: list of pair
        """
        if not self.tags:
            return []
        return self.tags

    def get_tags_as_list(self):
        """
        Get tags in list format.

        :return: list of tags
        :rtype: list of pair
        """
        return self.get_tags()

    def get_tags_as_map(self):
        """
        Get tags in map format.

        :return: tags in map format: {key: [list_of_val]}
        :rtype: dict of {str : list}
        """
        if not self.tags:
            return {}
        tag_map = {}
        for key, val in self.tags:
            if key not in tag_map:
                tag_map[key] = [val]
            else:
                tag_map[key].append(val)
        return tag_map
