import unittest
from opentracing import child_of
from wavefront_opentracing_python_sdk import WavefrontTracer
from wavefront_opentracing_python_sdk.reporting import ConsoleReporter


class TestSpanBuilder(unittest.TestCase):

    def test_ignore_active_span(self):
        tracer = WavefrontTracer(ConsoleReporter())
        scope = tracer.start_active_span("test_op")
        active_span = scope.span
        child_span = tracer.start_span(
            operation_name="child_op",
            references=child_of(active_span.context))
        active_trace_id = str(active_span.trace_id)
        child_trace_id = str(child_span.trace_id)
        self.assertEqual(active_trace_id, child_trace_id)

        child_span = tracer.start_span(
            operation_name="child_op",
            child_of=active_span,
            ignore_active_span=True)
        child_trace_id = str(child_span.trace_id)
        self.assertNotEqual(active_trace_id, child_trace_id)

    def test_multi_valued_tags(self):
        tracer = WavefrontTracer(ConsoleReporter())
        span = tracer.start_span("test_op", tags=[("key1", "val1"),
                                                  ("key1", "val2")])
        self.assertIsNotNone(span)
        self.assertIsNotNone(span.get_tags())
        self.assertIsNotNone(span.get_tags_as_list())
        self.assertIsNotNone(span.get_tags_as_map())
        self.assertTrue(1, len(span.get_tags_as_map()))
        self.assertTrue("val1" in span.get_tags_as_map().get("key1"))
        self.assertTrue("val2" in span.get_tags_as_map().get("key1"))
        span.finish()


if __name__ == '__main__':
    # run 'python -m unittest discover' from top-level to run tests
    unittest.main()
