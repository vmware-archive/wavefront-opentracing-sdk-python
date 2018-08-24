from wavefront_opentracing_python_sdk.reporting import Reporter


class CompositeReporter(Reporter):
    def __init__(self, *reporters):
        super(CompositeReporter, self).__init__(None)
        self.reporters = reporters

    def report(self, wavefront_span):
        for reporter in self.reporters:
            reporter.report()

    def get_failure_count(self):
        res = 0
        for reporter in self.reporters:
            res += reporter.get_failure_count()
        return res

    def close(self):
        for reporter in self.reporters:
            reporter.close()
