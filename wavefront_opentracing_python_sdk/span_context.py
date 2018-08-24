from opentracing import SpanContext


class WavefrontSpanContext(SpanContext):

    def __init__(self, trace_id, span_id, baggage=None):
        """
        Constructor of Wavefront Span Context
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
        return self._baggage or SpanContext.EMPTY_BAGGAGE

    def get_baggage_item(self, key):
        return self._baggage[key]

    def with_baggage_item(self, key, value):
        baggage = dict(self._baggage)
        baggage[key] = value
        return WavefrontSpanContext(self.trace_id, self.span_id, baggage)

    def get_trace_id(self):
        return self.trace_id

    def get_span_id(self):
        return self.span_id

    @property
    def has_trace(self):
        return self.trace_id and self.span_id

    def __str__(self):
        return 'WavefrontSpanContext{traceId=' + str(self.trace_id) + \
               ', spanId=' + str(self.span_id) + '}'
