
class Error:
    """Error statements"""

    @staticmethod
    def invalid_parameter(invalid_parameters: list):
        return f'{",".join(invalid_parameters)} are not a supported search parameter'

    @staticmethod
    def incomplet_lat_lon_radius():
        return f'Parameters lon, lat and radius have to be set together'
