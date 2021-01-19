from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from ccsi.config import Config

spec = APISpec(
    title="Copernicus Core Service Interface",
    version=Config.VERSION,
    openapi_version="3.0.2",
    info=dict(description="API Documentation"),
    plugins=[MarshmallowPlugin()],
)
