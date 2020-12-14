class _Validator:

    def __init__(self):
        self._report = None

    @property
    def report(self):
        """return dict with invalid parameters and error message. If None, parameters ar valid"""
        return self._report

    def validate(self, parameters, service_parameters):
        report = {key: service_parameters[key].validate(value) for key, value in parameters.items()
                  if service_parameters[key].validate(value) is not True}
        if len(report) > 0:
            self._report = report
            return False
        else:
            self._report = None
            return True

validator = _Validator()