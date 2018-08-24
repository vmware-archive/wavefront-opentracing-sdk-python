from wavefront_opentracing_python_sdk.reporting import Reporter
from wavefront_python_sdk import WavefrontDirectClient


class DirectTracingReporter(Reporter):
    def __init__(self, server, token, max_queue_size=50000,
                 batch_size=10000, flush_interval_seconds=5, source=None):
        self.sender = WavefrontDirectClient(
            server, token, max_queue_size, batch_size, flush_interval_seconds)
        self.source = source
        super(DirectTracingReporter, self).__init__(source)

    def report(self, wavefront_span):
        self.send_span(self.sender, wavefront_span)

    def get_failure_count(self):
        return self.sender.get_failure_count()

    def close(self):
        self.sender.close()
