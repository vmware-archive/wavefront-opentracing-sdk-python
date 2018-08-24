from wavefront_opentracing_python_sdk.propagation import Propagator

from uuid import UUID
from wavefront_opentracing_python_sdk import WavefrontSpanContext


class TextMapPropagator(Propagator):
    _BAGGAGE_PREFIX = "wf-ot-"
    _TRACE_ID = _BAGGAGE_PREFIX + "traceid"
    _SPAN_ID = _BAGGAGE_PREFIX + "spanid"

    def inject(self, span_context, carrier):
        carrier.update({self._TRACE_ID, str(span_context.get_trace_id)})
        carrier.update({self._SPAN_ID, str(span_context.get_span_id)})
        for key in span_context.baggage():
            carrier.update({self._BAGGAGE_PREFIX + key,
                            span_context.get_baggage_item(key)})

    def extract(self, carrier):
        trace_id = None
        span_id = None
        baggage = {}
        for key, val in carrier:
            key = key.lower()
            if key == self._TRACE_ID:
                trace_id = UUID(val)
            elif key == self._SPAN_ID:
                span_id = UUID(val)
            elif key.startswith(self._BAGGAGE_PREFIX):
                baggage.update({self.strip_prefix(key), val})

        if trace_id is None or span_id is None:
            return None

        return WavefrontSpanContext(trace_id, span_id, baggage)

    def strip_prefix(self, key):
        return key[len(self._BAGGAGE_PREFIX):]
