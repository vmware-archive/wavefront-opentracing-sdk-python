"""
Constant Sampler.

Sampler that allows spans through at a constant rate (all in or all out).

@author: Hao Song (songhao@vmware.com)
"""

from wavefront_opentracing_sdk.sampling.sampler import Sampler


# pylint: disable=useless-object-inheritance
class ConstantSampler(Sampler):
    """Tracing span constant sampler."""

    def __init__(self, decision):
        self._decision = decision
        self.set_decision(decision)

    def sample(self, operation_name, trace_id, duration):
        return self._decision

    def is_early(self):
        return True

    def set_decision(self, decision):
        """Sets the decision for this sampler."""
        self._decision = decision
