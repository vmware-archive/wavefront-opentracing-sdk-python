class Propagator(object):
    def extract(self, carrier):
        raise NotImplementedError

    def inject(self, span_context, carrier):
        raise NotImplementedError
