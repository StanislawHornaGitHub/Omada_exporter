from pydantic import BaseModel, Field
import src.Omada.Model.Labels.Port as Port
import src.Omada.helpers.modelFields as modelFields
import src.Omada.helpers.modelFields as modelFields
from src.Omada.Model.subModels.WanPortIpv6Config import WanPortIpv6Config
from src.Omada.Model.subModels.WanPortIpv4Config import WanPortIpv4Config


class RouterPort(BaseModel):
    name: str = Field(alias="gatewayName")
    mac: str
    port: int
    portName: str = Field(alias="name")
    portDesc: str = Field(default="null")
    mode: str
    ip: str = Field(default="null")
    poe: str = Field(default="False")
    linkStatus: str = Field(alias="status")
    internetState: str = Field(default="Offline")
    online: str = Field(alias="onlineDetection")
    linkSpeed: str = Field(alias="speed",)
    duplex: str
    tx: int
    rx: int
    protocol: str = Field(alias="proto", default="null")
    wanPortIpv6Config: WanPortIpv6Config = Field(default=None)
    wanPortIpv4Config: WanPortIpv4Config = Field(default=None)
    latency: int
    loss: float | None

    def __init__(self, **data):

        # port is disconnected
        if data["status"] == 0:
            data["mode"] = -1
            data["onlineDetection"] = 0
            data["speed"] = -1
            data["duplex"] = -1
            data["online"] = 0
            data["latency"] = 0
            data["loss"] = 1

        # port is in lan mode
        if data["mode"] == 1:
            data["portDesc"] = "downLink"
            data["onlineDetection"] = -1
            data["latency"] = 0
            data["loss"] = 0

        data["poe"] = str(data.get("poe", "null"))

        data = modelFields.map_data_values(data, Port.router_value_map)
        super().__init__(**data)
