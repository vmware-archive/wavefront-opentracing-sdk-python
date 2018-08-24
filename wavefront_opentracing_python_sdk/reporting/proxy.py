from wavefront_opentracing_python_sdk.reporting import Reporter
from wavefront_python_sdk import WavefrontProxyClient


class ProxyTracingReporter(Reporter):
    def __init__(self, proxy_host, metrics_port, distribution_port,
                 tracing_port, source=None):
        self.sender = WavefrontProxyClient(
            proxy_host, metrics_port, distribution_port, tracing_port)
        self.source = source
        super(ProxyTracingReporter, self).__init__(source)

    def report(self, wavefront_span):
        self.send_span(self.sender, wavefront_span)

    def get_failure_count(self):
        return self.sender.get_failure_count()

    def close(self):
        self.sender.close()
