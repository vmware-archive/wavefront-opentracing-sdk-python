# import os
# import random
# import time
import uuid
from opentracing import Tracer, ReferenceType
from opentracing.scope_managers import ThreadLocalScopeManager
from wavefront_opentracing_python_sdk.propagation import PropagatorRegistry
from wavefront_opentracing_python_sdk import WavefrontSpan, \
    WavefrontSpanContext, WavefrontReference


class WavefrontTracer(Tracer):
    def __init__(self, reporter, tags=None):
        super(WavefrontTracer, self).__init__(ThreadLocalScopeManager())
        self._reporter = reporter
        self._tags = tags or {}
        self.registry = PropagatorRegistry()
        # self.random = random.Random(time.time() * (os.getpid() or 1))

    def start_span(self,
                   operation_name=None,
                   child_of=None,
                   references=None,
                   tags=None,
                   start_time=None,
                   ignore_active_span=False):
        """

        :param operation_name:
        :param child_of:
        :type child_of: WavefrontSpanContext or WavefrontSpan
        :param references:
        :type references: :obj:`list` of :class:`WavefrontReference`
        :param tags:
        :param start_time:
        :param ignore_active_span:
        :return:
        """
        parents = []
        follows = []
        baggage = None

        parent = child_of
        if references:
            one_reference = references
            if isinstance(references, list):
                one_reference = references[0]
                for reference in references:
                    if reference.get_type() == ReferenceType.CHILD_OF:
                        parents.append(
                            reference.get_span_context().get_span_id())
                    elif reference.get_type() == ReferenceType.FOLLOWS_FROM:
                        follows.append(
                            reference.get_span_context().get_span_id())
            parent = one_reference.get_span_context()
        # allow Span to be passed as reference, not just SpanContext
        if isinstance(parent, WavefrontSpan):
            parent = parent.context

        if parent is None or not parent.has_trace:
            trace_id = uuid.uuid1()
            span_id = trace_id
            tags = tags or {}
            if parent and parent.baggage:
                baggage = dict(parent.baggage)
        else:
            trace_id = parent.trace_id
            span_id = uuid.uuid1()
        span_ctx = WavefrontSpanContext(trace_id, span_id, baggage)
        return WavefrontSpan(self, operation_name, span_ctx, start_time,
                             parents, follows, tags)

    def start_active_span(self,
                          operation_name,
                          child_of=None,
                          references=None,
                          tags=None,
                          start_time=None,
                          ignore_active_span=False,
                          finish_on_close=True):
        """

        :param operation_name:
        :param child_of:
        :type child_of: WavefrontSpanContext
        :param references:
        :param tags:
        :param start_time:
        :param ignore_active_span:
        :param finish_on_close:
        :return:
        """
        return self.scope_manager.activate(
            self.start_span(operation_name, child_of, references, tags,
                            start_time, ignore_active_span), finish_on_close)

    def inject(self, span_context, format, carrier):
        propagator = self.registry.get(format)
        if not propagator:
            raise TypeError("Invalid format " + str(format))
        if isinstance(span_context, WavefrontSpan):
            # be flexible and allow Span as argument, not only SpanContext
            span_context = span_context.context
        if not isinstance(span_context, WavefrontSpanContext):
            raise ValueError(
                'Expecting WavefrontSpanContext, not %s', type(span_context))
        propagator.update({span_context, carrier})

    def extract(self, format, carrier):
        propagator = self.registry.get(format)
        if not propagator:
            raise TypeError("Invalid format " + str(format))
        return propagator.extract(carrier)

    def close(self):
        self._reporter.close()

    def report_span(self, span):
        self._reporter.report(span)

    def _trace_ancestry(self):
        pass
