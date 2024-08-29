from pydantic import BaseModel, Field, field_serializer


from src.Omada.Model.subModels.ApWirelessUpLink import ApWirelessUpLink

class AccessPoint(BaseModel):
    deviceType: str = Field(default="AccessPoint")
    type: str
    mac: str
    name: str
    ip: str
    ipv6List: list[str] = Field(default=None)
    wlanId: str
    wireless_uplink_info: list[ApWirelessUpLink] = Field(default=None)
    model: str = Field(alias="showModel")
    firmwareVersion: str
    cpuUtil: int
    memUtil: int
    uptimeLong: int