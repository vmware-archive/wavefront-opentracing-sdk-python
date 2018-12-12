# wavefront-opentracing-sdk-python [![travis build status](https://travis-ci.com/wavefrontHQ/wavefront-opentracing-sdk-python.svg?branch=master)](https://travis-ci.com/wavefrontHQ/wavefront-opentracing-sdk-python)

This Python library provides open tracing support for Wavefront.

## Requirements

Python 2.7+ and Python 3.x are supported.

```bash
pip install wavefront-opentracing-sdk-python 
```
## Usage

### Application Tags

Application tags determine the metadata (span tags) that are included with every span reported to Wavefront. These tags enable you to filter and query trace data in Wavefront. Instantiating ApplicationTags as follows:

```python
from wavefront_sdk.common import ApplicationTags

application_tags = ApplicationTags(application="<APPLICATION>",
                                   service="<SERVICE>",
                                   cluster="<CLUSTER>",
                                   shard="<SHARD>",
                                   custom_tags=[("custom_key", "custom_val")])
```

### Tracer

OpenTracing Tracer is a simple, thin interface for Span creation and propagation across arbitrary transports.

#### How to instantiate a Wavefront tracer?

1. Set Up Application Tags

```python
tracer = WavefrontTracer(reporter=reporter, application_tags=application_tags)
```

#### Close the tracer
Before exiting your application, don't forget to close the tracer which will flush all the buffered spans to Wavefront.
```python
tracer.close()
```

When you instantiate the tracer, you should pass a customized reporter as shown below.

### WavefrontSpanReporter
Before we instantiate the `WavefrontSpanReporter`, we need to instantiate a Wavefront Client 
(i.e. either `WavefrontProxyClient` or `WavefrontDirectClient`).
Refer to this page (https://github.com/wavefrontHQ/wavefront-python-sdk/blob/master/README.md)
to instantiate `WavefrontProxyClient` or `WavefrontDirectClient`.

#### Option 1 - Proxy reporter using Wavefront Proxy Client
```python
from wavefront_sdk import WavefrontProxyClient
from wavefront_opentracing_sdk.reporting import WavefrontSpanReporter
from wavefront_opentracing_sdk import WavefrontTracer

# Report opentracing spans to Wavefront via a Wavefront Proxy.
proxy_client = WavefrontProxyClient(
    host="<PROXY_HOST>",
    tracing_port=30000,
    distribution_port=40000,
    metrics_port=2878
)
proxy_reporter = WavefrontSpanReporter(
    client=proxy_client,
    source="wavefront-tracing-example"
)

# Construct Wavefront opentracing Tracer using proxy reporter.
tracer = WavefrontTracer(reporter=proxy_reporter,
                         application_tags=application_tags) 

# To get failures observed while reporting.
total_failures = proxy_reporter.get_failure_count()
```

#### Option 2 - Direct reporter using Wavefront Direct Ingestion Client
```python
from wavefront_sdk import WavefrontDirectClient
from wavefront_opentracing_sdk.reporting import WavefrontSpanReporter
from wavefront_opentracing_sdk import WavefrontTracer

# Report opentracing spans to Wavefront via a Wavefront Direct Ingestion.
direct_client = WavefrontDirectClient(
    server="<SERVER_ADDR>",
    token="<TOKEN>"
)
direct_reporter = WavefrontSpanReporter(
    client=direct_client,
    source="wavefront-tracing-example"
)

# Construct Wavefront opentracing Tracer using direct reporter.
tracer = WavefrontTracer(reporter=direct_reporter,
                         application_tags=application_tags) 

# To get failures observed while reporting.
total_failures = direct_reporter.get_failure_count()
```

#### Composite reporter (chaining multiple reporters)
```PYTHON
from wavefront_opentracing_sdk.reporting import ConsoleReporter, CompositeReporter

# Creates a console reporter that reports span to stdout (useful for debugging).
console_reporter = ConsoleReporter(source="wavefront-tracing-example")

# Instantiate a composite reporter composed of console and direct reporter.
composite_reporter = CompositeReporter(direct_reporter, console_reporter)

# Construct Wavefront opentracing Tracer composed of console and direct reporter.
tracer = WavefrontTracer(reporter=composite_reporter,
                         application_tags=application_tags) 
```
