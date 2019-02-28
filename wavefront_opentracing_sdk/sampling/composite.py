"""
Composite Sampler.

Sampler that delegates to multiple other samplers for sampling.

The sampling decision is true if any of the delegate samplers allow the span.

@author: Hao Song (songhao@vmware.com)
"""

from wavefront_opentracing_sdk.sampling.sampler import Sampler


# pylint: disable=useless-object-inheritance
class CompositeSampler(Sampler):
    """Tracing span composite sampler."""

    def __init__(self, samplers):
        self.samplers = samplers

    def sample(self, operation_name, trace_id, duration):
        if not self.samplers:
            return True
        for sampler in self.samplers:
            if isinstance(sampler, Sampler):
                if sampler.sample(operation_name, trace_id, duration):
                    return True
        return False

    def is_early(self):
        return False
