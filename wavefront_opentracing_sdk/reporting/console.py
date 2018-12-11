"""
Console Reporter.

@author: Hao Song (songhao@vmware.com)
"""
from __future__ import print_function
from wavefront_sdk.common.utils import tracing_span_to_line_data
from wavefront_opentracing_sdk.reporting import reporter


class ConsoleReporter(reporter.Reporter):
    """Console Reporter.

    Used for print span data to console.
    """

    def report(self, wavefront_span):
        """
        Print span data to console.

        :param wavefront_span: Wavefront span to be reported
        """
        line_data = tracing_span_to_line_data(
            wavefront_span.get_operation_name(),
            int(wavefront_span.get_start_time() * 1000),
            int(wavefront_span.get_duration_time() * 1000),
            self.source,
            wavefront_span.trace_id,
            wavefront_span.span_id,
            wavefront_span.get_parents(),
            wavefront_span.get_follows(),
            wavefront_span.get_tags(),
            span_logs=None,
            default_source="unknown")
        print(line_data)

    def get_failure_count(self):
        """No-op."""
        return 0

    def close(self):
        """No-op."""
        return
