from opentracing import child_of
from wavefront_opentracing_python_sdk import WavefrontSpan, \
    WavefrontSpanContext, WavefrontTracer
from wavefront_python_sdk import WavefrontDirectClient

if __name__ == "__main__":
    reporter = WavefrontDirectClient("http://localhost:8080",
                                     "9ea0d7c3-311a-419b-86b1-7a515f4aff76")
    tracer = WavefrontTracer(reporter)
    span1 = tracer.start_span('span1')
    span2 = tracer.start_span(
        "span2",
        references=child_of(span1.context)
    )
