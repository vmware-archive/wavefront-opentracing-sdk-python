# wavefront-opentracing-sdk-python

[![travis build status](https://travis-ci.com/wavefrontHQ/wavefront-opentracing-sdk-python.svg?branch=master)](https://travis-ci.com/wavefrontHQ/wavefront-opentracing-sdk-python)
[![OpenTracing Badge](https://img.shields.io/badge/OpenTracing-enabled-blue.svg)](http://opentracing.io)
[![image](https://img.shields.io/pypi/v/wavefront-opentracing-sdk-python.svg)](https://pypi.org/project/wavefront-opentracing-sdk-python/)
[![image](https://img.shields.io/pypi/l/wavefront-opentracing-sdk-python.svg)](https://pypi.org/project/wavefront-opentracing-sdk-python/)
[![image](https://img.shields.io/pypi/pyversions/wavefront-opentracing-sdk-python.svg)](https://pypi.org/project/wavefront-opentracing-sdk-python/)

The Wavefront by VMware OpenTracing SDK for Python is a library that provides open tracing support for Wavefront.

## Requirements and Installation

Python 2.7+ and Python 3.x are supported.

```bash
pip install wavefront-opentracing-sdk-python
```
## Set Up a Tracer

[Tracer](https://github.com/opentracing/specification/blob/master/specification.md#tracer) is an OpenTracing [interface](https://github.com/opentracing/opentracing-java#initialization) for creating spans and propagating them across arbitrary transports.

This SDK provides a `WavefrontTracer` for creating spans and sending them to Wavefront. The steps for creating a `WavefrontTracer` are:
1. Create an `ApplicationTags` instance, which specifies metadata about your application.
2. Create a Wavefront sender object for sending trace data to Wavefront.
3. Create a `WavefrontSpanReporter` for reporting trace data to Wavefront.
4. Create the `WavefrontTracer` instance.

The following code sample creates a Tracer. For the details of each step, see the sections below.

```python
tracer = WavefrontTracer(reporter=reporter, application_tags=application_tags)
```


### 1. Set Up Application Tags

Application tags determine the metadata (span tags) that are included with every span reported to Wavefront. These tags enable you to filter and query trace data in Wavefront.

You encapsulate application tags in an `ApplicationTags` object. See [Instantiating ApplicationTags](https://github.com/wavefrontHQ/wavefront-sdk-python/blob/master/docs/apptags.md) for details.

### 2. Set Up a Wavefront Sender

A "Wavefront sender" is an object that implements the low-level interface for sending data to Wavefront. You can choose to send data using either the [Wavefront proxy](https://docs.wavefront.com/proxies.html) or [direct ingestion](https://docs.wavefront.com/direct_ingestion.html).

* If you have already set up a Wavefront sender for another SDK that will run in the same process, use that one.  (For details about sharing a Wavefront sender, see [Share a Wavefront Sender](https://github.com/wavefrontHQ/wavefront-sdk-python/blob/master/docs/sender.md#share-a-wavefront-sender).)

* Otherwise, follow the steps in [Set Up a Wavefront Sender](https://github.com/wavefrontHQ/wavefront-sdk-python/blob/master/docs/sender.md#set-up-a-wavefront-sender).



### 3. Set Up a Reporter
You must create a `WavefrontSpanReporter` to report trace data to Wavefront. You can optionally create a `CompositeReporter` to send data to Wavefront and to print to the console.

#### Create a WavefrontSpanReporter
To create a `WavefrontSpanReporter`:
* Specify the Wavefront sender from [Step 2](#2-set-up-a-wavefront-sender), i.e. either `WavefrontProxyClient` or `WavefrontDirectClient`.
* (Optional) Specify a string that represents the source for the reported spans. If you omit the source, the host name is automatically used.

To create a `WavefrontSpanReporter`:

```python
import wavefront_opentracing_sdk.reporting
from wavefront_sdk import WavefrontDirectClient
  # or
  # from wavefront_sdk import WavefrontProxyClient

wavefront_sender = ...   # see Step 2

wf_span_reporter = wavefront_opentracing_sdk.reporting.WavefrontSpanReporter(
    client=wavefront_sender,
    source='wavefront-tracing-example'   # optional nondefault source name
)

# To get failures observed while reporting.
total_failures = wf_span_reporter.get_failure_count()
```
**Note:** After you initialize the `WavefrontTracer` with the `WavefrontSpanReporter` (in step 4), completed spans will automatically be reported to Wavefront.
You do not need to start the reporter explicitly.

#### Create a CompositeReporter (Optional)
A `CompositeReporter` enables you to chain a `WavefrontSpanReporter` to another reporter, such as a `ConsoleReporter`. A console reporter is useful for debugging.

```PYTHON
from wavefront_opentracing_sdk.reporting import CompositeReporter
from wavefront_opentracing_sdk.reporting import ConsoleReporter
from wavefront_opentracing_sdk.reporting import WavefrontSpanReporter

wf_span_reporter = ...

# Create a console reporter that reports span to stdout
console_reporter = ConsoleReporter(source='wavefront-tracing-example')

# Instantiate a composite reporter composed of console and WavefrontSpanReporter.
composite_reporter = CompositeReporter(wf_span_reporter, console_reporter)
```
### 4. Create the WavefrontTracer

To create a `WavefrontTracer`, you pass the `ApplicationTags` and `Reporter` instances you created in the previous steps:

```PYTHON
import wavefront_opentracing_sdk

from wavefront_opentracing_sdk.reporting import WavefrontSpanReporter
from wavefront_sdk.common import ApplicationTags
from wavefront_sdk import WavefrontDirectClient
  # or
  # from wavefront_sdk import WavefrontProxyClient

application_tags = ...   # see Step 1 above
wf_span_reporter = ...   # see Step 3 above

# Construct Wavefront opentracing Tracer
tracer = wavefront_opentracing_sdk.WavefrontTracer(
    reporter=wf_span_reporter,
    application_tags=application_tags)
```

#### Close the Tracer
Always close the tracer before exiting your application to flush all buffered spans to Wavefront.

```python
tracer.close()
```
## Cross Process Context Propagation
See the [context propagation documentation](https://github.com/wavefrontHQ/wavefront-opentracing-sdk-python/tree/master/docs/contextpropagation.md) for details on propagating span contexts across process boundaries.

## RED Metrics
See the [RED metrics documentation](https://github.com/wavefrontHQ/wavefront-opentracing-sdk-python/blob/master/docs/metrics.md) for details on the out-of-the-box metrics and histograms that are provided.
