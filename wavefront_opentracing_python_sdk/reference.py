from opentracing import Reference


class WavefrontReference(Reference):

    def __init__(self, context, reference_type):
        """

        :param context:
        :type context: wavefront_opentracing_python_sdk.WavefrontSpanContext
        :param reference_type:
        :type reference_type: opentracing.ReferenceType
        """
        self.context = context
        self.type = reference_type

    def get_span_context(self):
        return self.context

    def get_type(self):
        return self.reference_type
