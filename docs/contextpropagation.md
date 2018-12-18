# Cross-Process Context Propagation

Following the [OpenTracing standard](https://opentracing.io/docs/overview/inject-extract/), you must arrange for your applicaton's `Tracer` to propagate a span context across process boundaries whenever a client microservice sends a request to another microservice. Doing so enables you to represent the client's request as part of a continuing trace that consists of multiple connected spans. 

The `Tracer` provides `inject` and `extract` methods for propagating span contexts across process boundaries. You can use these methods to propagate a `childOf` or `followsFrom` relationship between spans across process or host boundaries.

* In code that makes an external call (such as an HTTP invocation), obtain the current span and its span context, create a carrier, and inject the span context into the carrier:
  
```python
current_span = ...  # obtain the current span
headers = {'URL': "http://localhost", 'METHOD': "GET"}
tracer.inject(current_span, Format.HTTP_HEADERS, headers)
# loop over the injected text map and set its contents on the HTTP request header...
```

* In code that responds to the call (i.e., that receives the HTTP request), extract the propagated span context:
```python
span_ctx = tracer.extract(Format.HTTP_HEADERS, headers)
with tracer.start_active_span('child_span', child_of=span_ctx):
	# ...
```

