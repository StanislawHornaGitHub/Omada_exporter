from pydantic import BaseModel, Field, field_serializer
import datetime
import src.Omada.helpers.timeFunctions as timeHelpers

from src.Omada.Model.subModels.SwitchPort import SwitchPort

class Switch(BaseModel):
    deviceType: str = Field(default="Switch")
    name: str
    mac: str
    ip: str
    ipv6List: list[str]
    model: str
    firmwareVersion: str
    version: str
    hwVersion: str
    cpuUtil: int
    memUtil: int
    uptime: str
    portList: list[SwitchPort]
