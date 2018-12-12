"""
Propagator Registry.

@author: Hao Song (songhao@vmware.com)
"""
from opentracing.propagation import Format
from wavefront_opentracing_sdk.propagation import textmap, http


# pylint: disable=useless-object-inheritance
class PropagatorRegistry(object):
    """Registry of available propagators."""

    def __init__(self):
        """Construct propagator registry."""
        self.propagators = {Format.TEXT_MAP: textmap.TextMapPropagator(),
                            Format.HTTP_HEADERS: http.HTTPPropagator()}

    # pylint: disable=redefined-builtin
    def get(self, format):
        """
        Get propagator of certain format.

        :param format: Format of propagator.
        :type format: opentracing.propagation.Format
        :return: Propagator of given format
        :rtype: wavefront_opentracing_sdk.propagation.Propagator
        """
        return self.propagators.get(format)

    # pylint: disable=redefined-builtin
    def register(self, format, propagator):
        """
        Register propagator.

        :param format: Format of propagator.
        :type format: opentracing.propagation.Format
        :param propagator: Propagator to be registered.
        :type propagator: Propagator
        """
        self.propagators.update({format: propagator})
