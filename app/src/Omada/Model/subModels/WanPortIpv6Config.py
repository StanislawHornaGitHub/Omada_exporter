from pydantic import BaseModel, Field
import src.Omada.helpers.modelFields as modelFields

value_map: dict[str, dict] = {
    "enable": {
        0: "disconnected",
        1: "connected",
    },
    "internetState": {
        0: "disconnected",
        1: "connected",
    }
}


class WanPortIpv6Config(BaseModel):
    enable: str
    proto: str = Field(default="null")
    addr: str
    gateway: str
    priDns: str
    sndDns: str
    internetState: str = Field(default="null")
    portMac: str = Field(default="null", alias="mac")

    def __init__(self, **data):
        data = modelFields.map_data_values(data, value_map)
        super().__init__(**data)
