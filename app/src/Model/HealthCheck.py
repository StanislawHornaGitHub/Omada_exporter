from pydantic import BaseModel, Field

class HealthCheck(BaseModel):
    UserSession: bool
    OpenAPI: bool
    ControllerName: str
    ControllerVersion: str