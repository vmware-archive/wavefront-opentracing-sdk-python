"""
HTTP Propagator.

@author: Hao Song (songhao@vmware.com)
"""
from wavefront_opentracing_python_sdk.propagation import TextMapPropagator


class HTTPPropagator(TextMapPropagator):
    """HTTP Propagator."""

    pass
