"""
Unit Tests for Wavefront Span.

@author: Hao Song (songhao@vmware.com)
"""
import unittest
from wavefront_sdk.common import ApplicationTags
from wavefront_opentracing_sdk import WavefrontTracer
from wavefront_opentracing_sdk.reporting import ConsoleReporter


class TestSpan(unittest.TestCase):
    """Unit Tests for Wavefront Span."""
    application_tags = ApplicationTags(application="app",
                                       service="service",
                                       cluster="us-west-1",
                                       shard="primary",
                                       custom_tags=[("custom_k", "custom_v")])

    def test_ignore_active_span(self):
        """Test Ignore Active Span."""
        tracer = WavefrontTracer(ConsoleReporter(), self.application_tags)
        scope = tracer.start_active_span("test_op")
        active_span = scope.span

        # Span created with ignore_active_span=False by default.
        child_span = tracer.start_span(
            operation_name="child_op",
            ignore_active_span=False)
        active_trace_id = str(active_span.trace_id)
        child_trace_id = str(child_span.trace_id)
        self.assertEqual(active_trace_id, child_trace_id)
        child_span.finish()

        # Span created with ignore_active_span=True.
        child_span = tracer.start_span(
            operation_name="child_op",
            ignore_active_span=True)
        child_trace_id = str(child_span.trace_id)
        self.assertNotEqual(active_trace_id, child_trace_id)
        child_span.finish()

        scope.close()
        tracer.close()

    def test_multi_valued_tags(self):
        """Test Multi-valued Tags."""
        tracer = WavefrontTracer(ConsoleReporter(), self.application_tags)
        span = tracer.start_span("test_op", tags=[("key1", "val1"),
                                                  ("key1", "val2")])
        self.assertIsNotNone(span)
        self.assertIsNotNone(span.get_tags())
        self.assertIsNotNone(span.get_tags_as_list())
        self.assertIsNotNone(span.get_tags_as_map())
        self.assertEqual(6, len(span.get_tags_as_map()))
        self.assertTrue("app" in span.get_tags_as_map().get("application"))
        self.assertTrue("service" in span.get_tags_as_map().get("service"))
        self.assertTrue("us-west-1" in span.get_tags_as_map().get("cluster"))
        self.assertTrue("primary" in span.get_tags_as_map().get("shard"))
        self.assertTrue("custom_v" in span.get_tags_as_map().get("custom_k"))
        self.assertTrue("val1" in span.get_tags_as_map().get("key1"))
        self.assertTrue("val2" in span.get_tags_as_map().get("key1"))
        span.finish()
        tracer.close()


if __name__ == '__main__':
    # run 'python -m unittest discover' from top-level to run tests
    unittest.main()
