from pydantic import BaseModel, Field


class RouterPortStats(BaseModel):
    name: str = Field(alias="gatewayName")
    mac: str
    port: int
    txRate: int = Field(alias="tx")
    rxRate: int = Field(alias="rx")
    txPkts: int
    rxPkts: int
    dropPkts: int
    errPkts: int
