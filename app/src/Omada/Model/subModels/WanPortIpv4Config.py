from pydantic import BaseModel, Field


class WanPortIpv4Config(BaseModel):
    ip: str
    ip2: str = Field(default="null")
    gateway: str
    gateway2: str
    priDns: str
    sndDns: str
    priDns2: str
    sndDns2: str
    portMac: str = Field(default="null", alias="mac")
