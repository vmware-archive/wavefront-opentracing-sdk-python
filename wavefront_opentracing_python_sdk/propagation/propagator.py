from wavefront_opentracing_python_sdk.propagation import Extractor
from wavefront_opentracing_python_sdk.propagation import Injector


class Propagator(Extractor, Injector):
    def extract(self, carrier):
        raise NotImplementedError

    def inject(self, span_context, carrier):
        raise NotImplementedError
