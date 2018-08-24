class Reporter(object):

    def __init__(self, source):
        self.source = source

    def report(self, wavefront_span):
        raise NotImplementedError

    def get_failure_count(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def send_span(self, sender, wavefront_span):
        try:
            sender.send_span(
                wavefront_span.get_operation_name(),
                wavefront_span.get_start_time_micros() / 1000,
                wavefront_span.get_duration_time_micros() / 1000,
                self.source,
                wavefront_span.trace_id,
                wavefront_span.span_id,
                list(map(lambda p: p.get_span_context().get_span_id(),
                         wavefront_span.get_parents())),
                list(map(lambda f: f.get_span_context().get_span_id(),
                         wavefront_span.get_follows())),
                wavefront_span.get_tags(),
                span_logs=None)
        except (AttributeError, TypeError) as error:
            print("Invalid Sender, no valid send_span()")
            raise error
