"""
Unit Tests for Wavefront Tracer.

@author: Hao Song (songhao@vmware.com)
"""
import unittest
from opentracing.propagation import Format
from wavefront_sdk.common import ApplicationTags
from wavefront_opentracing_sdk import WavefrontTracer
from wavefront_opentracing_sdk.reporting import ConsoleReporter


class TestTracer(unittest.TestCase):
    """Unit Tests for Wavefront Tracer."""
    application_tags = ApplicationTags(application="app",
                                       service="service",
                                       cluster="us-west-1",
                                       shard="primary",
                                       custom_tags=[("custom_k", "custom_v")])

    def test_inject_extract(self):
        """Test Inject / Extract."""
        tracer = WavefrontTracer(ConsoleReporter(), self.application_tags)
        span = tracer.start_span('test_op')
        self.assertIsNotNone(span)
        span.set_baggage_item("customer", "test_customer")
        span.set_baggage_item("request_type", "mobile")
        carrier = {}
        tracer.inject(span.context, Format.TEXT_MAP, carrier)
        span.finish()
        ctx = tracer.extract(Format.TEXT_MAP, carrier)
        self.assertEqual("test_customer", ctx.get_baggage_item("customer"))
        self.assertEqual("mobile", ctx.get_baggage_item("request_type"))

    def test_active_span(self):
        """Test Active Span."""
        tracer = WavefrontTracer(ConsoleReporter(), self.application_tags)
        span = tracer.start_span("test_op_1")
        self.assertIsNotNone(span)
        span.finish()
        scope = tracer.start_active_span("test_op_2", finish_on_close=True)
        self.assertIsNotNone(scope)
        self.assertIsNotNone(scope.span)
        scope.close()

    def test_global_tags(self):
        """Test Global Tags."""
        global_tags = [("foo1", "bar1"), ("foo2", "bar2")]
        tracer = WavefrontTracer(ConsoleReporter(), self.application_tags,
                                 global_tags)
        span = tracer.start_span(operation_name="test_op",
                                 tags=[("foo3", "bar3")])
        self.assertIsNotNone(span)
        self.assertIsNotNone(span.get_tags())
        self.assertIsNotNone(span.get_tags_as_list())
        self.assertIsNotNone(span.get_tags_as_map())
        self.assertEqual(8, len(span.get_tags()))
        self.assertTrue("app" in span.get_tags_as_map().get("application"))
        self.assertTrue("service" in span.get_tags_as_map().get("service"))
        self.assertTrue("us-west-1" in span.get_tags_as_map().get("cluster"))
        self.assertTrue("primary" in span.get_tags_as_map().get("shard"))
        self.assertTrue("custom_v" in span.get_tags_as_map().get("custom_k"))
        self.assertTrue("bar1" in span.get_tags_as_map().get("foo1"))
        self.assertTrue("bar2" in span.get_tags_as_map().get("foo2"))
        self.assertTrue("bar3" in span.get_tags_as_map().get("foo3"))
        span.finish()
        tracer.close()

    def test_global_multi_valued_tags(self):
        """Test Global Multi-valued Tags."""
        global_tags = [("key1", "val1"), ("key1", "val2")]
        tracer = WavefrontTracer(ConsoleReporter(), self.application_tags,
                                 global_tags)
        span = tracer.start_span(operation_name="test_op")
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
