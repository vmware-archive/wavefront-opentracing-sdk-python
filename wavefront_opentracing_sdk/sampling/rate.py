"""
Rate Sampler.

Sampler that allows a certain probabilistic rate (between 0.0 and 1.0) of spans
to be reported.

Note: Sampling is performed per trace id. All spans for a sampled trace will be
reported.

@author: Hao Song (songhao@vmware.com)
"""

from wavefront_opentracing_sdk.sampling.sampler import Sampler


# pylint: disable=useless-object-inheritance
class RateSampler(Sampler):
    """Tracing span rate sampler."""

    def __init__(self, sampling_rate):
        self._boundary = None
        self._MIN_SAMPLING_RATE = 0.0
        self._MAX_SAMPLING_RATE = 1.0
        self._MOD_FACTOR = 10000
        self.set_sampling_rate(sampling_rate)

    def sample(self, operation_name, trace_id, duration):
        return abs(trace_id % self._MOD_FACTOR) <= self._boundary

    def is_early(self):
        return True

    def set_sampling_rate(self, sampling_rate):
        """Sets the sampling rate for this sampler."""
        if sampling_rate < self._MIN_SAMPLING_RATE or \
                sampling_rate > self._MAX_SAMPLING_RATE:
            raise ValueError("sampling rate must be between %s and %s" % (
                self._MIN_SAMPLING_RATE, self._MAX_SAMPLING_RATE))
        self._boundary = sampling_rate * self._MOD_FACTOR
