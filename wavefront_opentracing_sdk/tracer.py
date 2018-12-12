"""
Wavefront Tracer.

@author: Hao Song (songhao@vmware.com)
"""

import time
import uuid
import opentracing
from opentracing.scope_managers import ThreadLocalScopeManager
from wavefront_opentracing_sdk.propagation import registry
from wavefront_opentracing_sdk.span import WavefrontSpan
from wavefront_opentracing_sdk.span_context import WavefrontSpanContext


class WavefrontTracer(opentracing.Tracer):
    """Wavefront Tracer."""

    def __init__(self, reporter, application_tags, global_tags=None):
        """
        Construct Wavefront Tracer.

        :param reporter: Reporter
        :type reporter: :class:`Reporter`
        :param application_tags: Application Tags
        :type application_tags: :class:`ApplicationTags`
        :param global_tags: Global tags for the tracer
        :type global_tags: list of pair
        """
        super(WavefrontTracer, self).__init__(ThreadLocalScopeManager())
        self._reporter = reporter
        self._tags = global_tags or []
        self._tags.extend(application_tags.get_as_list())
        self.registry = registry.PropagatorRegistry()

    # pylint: disable=too-many-arguments,too-many-locals,too-many-branches
    def start_span(self,
                   operation_name=None,
                   child_of=None,
                   references=None,
                   tags=None,
                   start_time=None,
                   ignore_active_span=False):
        r"""
        Start and return a new :class:`Span` representing a unit of work.

        :param operation_name: Operation Name
        :type operation_name: str
        :param child_of: (optional) a WavefrontSpan or WavefrontSpanContext
            instance representing the parent in a REFERENCE_CHILD_OF reference.
            If specified, the `references` parameter must be omitted.
        :type child_of: WavefrontSpanContext or WavefrontSpan
        :param references: (optional) references that identify one or more
            parent :class:`SpanContext`\ s. (See the Reference documentation
            for detail).
        :type references: `list` of `opentracing.Reference`
        :param tags: an optional list of tags.
        :type tags: list of pair
        :param start_time: an explicit Span start time as a unix timestamp per
            :meth:`time.time()`
        :type start_time: float
        :param ignore_active_span: an explicit flag that ignores the current
            active :class:`Scope` and creates a root :class:`Span`.
        :type ignore_active_span: bool
        :return: an already-started :class:`WavefrontSpan` instance.
        :rtype: WavefrontSpan
        """
        parents = []
        follows = []
        baggage = None
        tags = tags or []
        tags.extend(self._tags)
        start_time = start_time or time.time()

        parent = None
        if child_of is not None:
            parent = child_of
            # allow both Span and SpanContext to be passed as child_of
            if isinstance(parent, WavefrontSpan):
                parent = child_of.context
            parents.append(parent.get_span_id())
        # references filed will be omitted if child_of field is not None
        elif parent is None and references:
            # allow both single Reference and list of Reference to be passed
            if not isinstance(references, list):
                references = [references]
            for reference in references:
                if isinstance(reference, opentracing.Reference):
                    reference_ctx = reference.referenced_context
                    # allow both Span and SpanContext to be passed as reference
                    if isinstance(reference_ctx, WavefrontSpan):
                        reference_ctx = reference_ctx.context
                    if parent is None:
                        parent = reference_ctx
                    if reference.type == opentracing.ReferenceType.CHILD_OF:
                        parents.append(reference_ctx.get_span_id())
                    elif reference.type == \
                            opentracing.ReferenceType.FOLLOWS_FROM:
                        follows.append(reference_ctx.get_span_id())

        if parent is None or not parent.has_trace:
            if not ignore_active_span and self.active_span is not None:
                parents.append(self.active_span.span_id)
                trace_id = self.active_span.trace_id
                span_id = uuid.uuid1()
            else:
                trace_id = uuid.uuid1()
                span_id = trace_id
            if parent and parent.baggage:
                baggage = dict(parent.baggage)
        else:
            trace_id = parent.trace_id
            span_id = uuid.uuid1()
        span_ctx = WavefrontSpanContext(trace_id, span_id, baggage)
        return WavefrontSpan(self, operation_name, span_ctx, start_time,
                             parents, follows, tags)

    # pylint: disable=too-many-arguments
    def start_active_span(self,
                          operation_name,
                          child_of=None,
                          references=None,
                          tags=None,
                          start_time=None,
                          ignore_active_span=False,
                          finish_on_close=True):
        r"""Return a newly started and activated :class:`Scope`.

        :param operation_name: Operation Name
        :type operation_name: str
        :param child_of: Parent Span
        :type child_of: WavefrontSpanContext or WavefrontSpan
        :param references: (optional) references that identify one or more
            parent :class:`SpanContext`\ s. (See the Reference documentation
            for detail).
        :type references: `list` of `opentracing.Reference`
        :param tags: an optional list of tags.
        :type tags: list of pair
        :param start_time: an explicit Span start time as a unix timestamp per
            :meth:`time.time()`
        :type start_time: float
        :param ignore_active_span: an explicit flag that ignores the current
            active :class:`Scope` and creates a root :class:`Span`.
        :type ignore_active_span: bool
        :param finish_on_close:
        :type finish_on_close:
        :return: a :class:`Scope`, already registered via the
            :class:`ScopeManager`.
        :rtype: opentracing.Scope
        """
        return self.scope_manager.activate(
            self.start_span(operation_name, child_of, references, tags,
                            start_time, ignore_active_span), finish_on_close)

    # pylint: disable=redefined-builtin
    def inject(self, span_context, format, carrier):
        """Inject `span_context` into `carrier`.

        The type of `carrier` is determined by `format`. See the
        :class:`Format` class/namespace for the built-in OpenTracing formats.

        Implementations *must* raise :exc:`UnsupportedFormatException` if
        `format` is unknown or disallowed.

        :param span_context: the :class:`SpanContext` instance to inject
        :type span_context: SpanContext

        :param format: a python object instance that represents a given
            carrier format. `format` may be of any type, and `format` equality
            is defined by python ``==`` equality.
        :type format: Format
        :param carrier: the format-specific carrier object to inject into
        """
        propagator = self.registry.get(format)
        if not propagator:
            raise opentracing.UnsupportedFormatException(
                "Invalid format " + str(format))
        if isinstance(span_context, WavefrontSpan):
            # be flexible and allow Span as argument, not only SpanContext
            span_context = span_context.context
        if not isinstance(span_context, WavefrontSpanContext):
            raise TypeError(
                'Expecting WavefrontSpanContext, not ' + type(span_context))
        propagator.inject(span_context, carrier)

    # pylint: disable=redefined-builtin
    def extract(self, format, carrier):
        """Return a :class:`SpanContext` instance extracted from a `carrier`.

        :param format: a python object instance that represents a given
            carrier format. `format` may be of any type, and `format` equality
            is defined by python ``==`` equality.
        :type format: opentracing.Format
        :param carrier: the format-specific carrier object to extract from
        :type carrier: dict
        :return: a :class:`SpanContext` extracted from `carrier` or ``None`` if
            no such :class:`SpanContext` could be found.
        :rtype: SpanContext
        """
        propagator = self.registry.get(format)
        if not propagator:
            raise opentracing.UnsupportedFormatException(
                "Invalid format " + str(format))
        return propagator.extract(carrier)

    def close(self):
        """Close the reporter to close the tracer."""
        self._reporter.close()

    def report_span(self, span):
        """Report span through the reporter."""
        self._reporter.report(span)
