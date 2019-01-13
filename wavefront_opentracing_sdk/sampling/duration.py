"""
Duration Sampler.

Sampler that allows spans above a given duration in milliseconds to be
reported.

@author: Hao Song (songhao@vmware.com)
"""

from wavefront_opentracing_sdk.sampling.sampler import Sampler


# pylint: disable=useless-object-inheritance
class DurationSampler(Sampler):
    """Tracing span duration sampler."""

    def __init__(self, duration):
        self._duration = None
        self.set_duration(duration)

    def sample(self, operation_name, trace_id, duration):
        return duration > self._duration

    def is_early(self):
        return False

    def set_duration(self, duration):
        self._duration = duration
