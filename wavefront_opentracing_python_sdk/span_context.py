"""
Wavefront Span Context.

@author: Hao Song (songhao@vmware.com)
"""
from opentracing import SpanContext


class WavefrontSpanContext(SpanContext):
    """Wavefront Span Context."""

    def __init__(self, trace_id, span_id, baggage=None):
        """
        Construct Wavefront Span Context.

        :param trace_id: Trace ID
        :type trace_id: uuid.UUID
        :param span_id: Span ID
        :type span_id: uuid.UUID
        :param baggage: Baggage
        :type baggage: dict
        """
        self.trace_id = trace_id
        self.span_id = span_id
        self._baggage = baggage or SpanContext.EMPTY_BAGGAGE

    @property
    def baggage(self):
        """Baggage of WavefrontSpan."""
        return self._baggage or SpanContext.EMPTY_BAGGAGE

    def get_baggage_item(self, key):
        """
        Get baggage item with key.

        :param key: Baggage key
        :return: Baggage value
        :rtype: str
        """
        return self._baggage[key]

    def with_baggage_item(self, key, value):
        """
        Create new span context with new dict of baggage and append item.

        :param key: key of the baggage item
        :type key: str
        :param value: value of the baggage item
        :type value: str
        :return: Span context itself
        :rtype: WavefrontSpanContext
        """
        baggage = dict(self._baggage)
        baggage[key] = value
        return WavefrontSpanContext(self.trace_id, self.span_id, baggage)

    def get_trace_id(self):
        """
        Get trace id from span context.

        :return: trace id of span context
        :rtype: uuid.UUID
        """
        return self.trace_id

    def get_span_id(self):
        """
        Get span id from span context.

        :return: span id of span context
        :rtype: uuid.UUID
        """
        return self.span_id

    @property
    def has_trace(self):
        """
        Return whether span context has both trace id and span id.

        :return: whether span context has both trace id and span id
        :rtype: bool
        """
        return self.trace_id and self.span_id

    def __str__(self):
        """
        Override __str__ func.

        :return: span context to string
        :rtype: str
        """
        return 'WavefrontSpanContext{{traceId={}, spanId={}}}'.format(
            self.trace_id, self.span_id)
