from wavefront_opentracing_python_sdk.reporting import Reporter
from wavefront_python_sdk.common.utils import tracing_span_to_line_data


class ConsoleReporter(Reporter):
    def __init__(self, source):
        super(ConsoleReporter, self).__init__(source)

    def report(self, wavefront_span):
        line_data = tracing_span_to_line_data(
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
            span_logs=None,
            default_source="unknown")
        print(line_data)

    def get_failure_count(self):
        # No-op
        return 0

    def close(self):
        # No-op
        return
