class Service:

    def __init__(self, service_name, parameters, mapped, connection, response_parser):
        self._parameters = parameters
        self.mapped = mapped
        self.connection = connection
        self.service_name = service_name
        self.response_parser = response_parser

    @classmethod
    def create(cls, service_name, parameters, mapped, connection, response_parser):
        return cls(service_name, parameters, mapped, connection, response_parser)

    def send_request(self, request: dict):
        """
        sending request to service, return list on entry elements
        request contain base api keys
        """
        service_request = self.translate(request)
        query = self.transform(service_request)
        validation = self.validate(query)
        if validation is True:
            response = self.connection.send_request(query)
            if response.status_code != 200:
                return {'Connection fail': f'{self.service_name}:{response.status_code}'}
            return self.response_parser.parse_response(response)
        else:
            return validation

    def translate(self, request: dict):
        """find common parameters between service and base api and return dict with corresponding api parameters name
        """
        common_params = {name for name in self.mapped.keys()}.intersection({name for name in request.keys()})
        return {self.mapped.get(param): request.get(param) for param in common_params .__iter__()}

    def transform(self, service_request: dict):
        """transform value of base api into value expected by service"""
        return {name: self.parameter(name).transform(value) for name, value in service_request.items()}

    def validate(self, service_request: dict):
        """Validation of query parameters against types expected by service api parameters """
        report = {name: self.parameter(name).validate(value) for name, value in service_request.items()
                  if self.parameter(name).validate(value) is not True}
        if len(report) > 0:
            return report
        else:
            return True

    def parameter(self, name):
        """call service parameter by original name"""
        return self._parameters.parameter(name)

    def input_parameter(self, name):
        """call service parameter by original name"""
        return self._parameters.parameter(self.mapped.get(name))

    def __hash__(self):
        return hash(self.service_name)

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and self.__hash__() == other.__hash__())
