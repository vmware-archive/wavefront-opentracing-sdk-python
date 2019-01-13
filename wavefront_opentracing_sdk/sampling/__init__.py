"""
Sampling Module.

@author: Hao Song (songhao@vmware.com)
"""
from wavefront_opentracing_sdk.sampling.rate import RateSampler
from wavefront_opentracing_sdk.sampling.duration import DurationSampler
from wavefront_opentracing_sdk.sampling.constant import ConstantSampler
from wavefront_opentracing_sdk.sampling.composite import CompositeSampler
