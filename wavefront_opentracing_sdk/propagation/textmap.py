"""
TextMap Propagator.

@author: Hao Song (songhao@vmware.com)
"""
from uuid import UUID

from wavefront_opentracing_sdk.propagation import propagator
from wavefront_opentracing_sdk.span_context import WavefrontSpanContext


class TextMapPropagator(propagator.Propagator):
    """Propagate contexts within TextMaps."""

    _BAGGAGE_PREFIX = "wf-ot-"
    _TRACE_ID = _BAGGAGE_PREFIX + "traceid"
    _SPAN_ID = _BAGGAGE_PREFIX + "spanid"

    def inject(self, span_context, carrier):
        """
        Inject the given Span Context into TextMap Carrier.

        :param span_context: Wavefront Span Context to be injected
        :type span_context: WavefrontSpanContext
        :param carrier: Carrier
        :type carrier: dict
        """
        if not isinstance(carrier, dict):
            raise TypeError('Carrier not a text map collection.')
        carrier.update({self._TRACE_ID: str(span_context.get_trace_id())})
        carrier.update({self._SPAN_ID: str(span_context.get_span_id())})
        for key, val in span_context.baggage.items():
            carrier.update({self._BAGGAGE_PREFIX + key: val})

    def extract(self, carrier):
        """
        Extract wavefront span context from the given carrier.

        :param carrier: Carrier
        :type carrier: dict
        :return: Wavefront Span Context
        :rtype: WavefrontSpanContext
        """
        trace_id = None
        span_id = None
        baggage = {}
        if not isinstance(carrier, dict):
            raise TypeError('Carrier not a text map collection.')
        for key, val in carrier.items():
            key = key.lower()
            if key == self._TRACE_ID:
                trace_id = UUID(val)
            elif key == self._SPAN_ID:
                span_id = UUID(val)
            elif key.startswith(self._BAGGAGE_PREFIX):
                baggage.update({self.strip_prefix(key): val})
        if trace_id is None or span_id is None:
            return None
        return WavefrontSpanContext(trace_id, span_id, baggage)

    def strip_prefix(self, key):
        """
        Strip the prefix of baggage items.

        :param key: Baggage item to be striped
        :type key: str
        :return: Striped baggage item
        :rtype: str
        """
        return key[len(self._BAGGAGE_PREFIX):]
