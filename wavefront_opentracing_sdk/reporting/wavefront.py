"""
Wavefront Span Reporter.

@author: Hao Song (songhao@vmware.com)
"""
import logging
from wavefront_opentracing_sdk.reporting import reporter


class WavefrontSpanReporter(reporter.Reporter):
    """Wavefront Span Reporter."""

    def __init__(self, client, source=None):
        """
        Construct Wavefront Span Reporter.

        :param client: Wavefront Client
        :type client: WavefrontProxyClient or WavefrontDirectClient
        :param source: Source of the reporter
        :type source: str
        """
        self.sender = client
        super(WavefrontSpanReporter, self).__init__(source)

    def report(self, wavefront_span):
        """
        Report span data via Wavefront Client.

        :param wavefront_span: Wavefront Span to be reported.
        """
        try:
            self.sender.send_span(
                wavefront_span.get_operation_name(),
                int(wavefront_span.get_start_time() * 1000),
                int(wavefront_span.get_duration_time() * 1000),
                self.source,
                wavefront_span.trace_id,
                wavefront_span.span_id,
                wavefront_span.get_parents(),
                wavefront_span.get_follows(),
                wavefront_span.get_tags(),
                span_logs=None)
        except (AttributeError, TypeError) as error:
            logging.error("Invalid Sender, no valid send_span function.")
            raise error

    def get_failure_count(self):
        """
        Get failure count from wavefront client.

        :return: Failure count
        :rtype: int
        """
        return self.sender.get_failure_count()

    def close(self):
        """Close the wavefront client."""
        self.sender.close()
