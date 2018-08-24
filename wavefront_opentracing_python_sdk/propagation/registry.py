from opentracing.propagation import Format
from wavefront_opentracing_python_sdk.propagation import TextMapPropagator, \
    HTTPPropagator


class PropagatorRegistry(object):
    def __init__(self):
        self.propagators = {Format.TEXT_MAP: TextMapPropagator(),
                            Format.HTTP_HEADERS: HTTPPropagator()}

    def get(self, format):
        return self.propagators.get(format)

    def register(self, format, propagator):
        self.propagators.update({format, propagator})
