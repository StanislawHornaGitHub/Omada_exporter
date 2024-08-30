from pydantic import BaseModel, Field


class AccessPointRadioStats(BaseModel):
    name: str = Field(alias="accessPointName")
    mac: str = Field(alias="accessPointMac")
    frequency: str
    tx: int
    rx: int
    # txPkts: int
    # rxPkts: int
    # txDropPkts: int
    # rxDropPkts: int
    txRetryPkts: int
    rxRetryPkts: int
    # txErrPkts: int
    # rxErrPkts: int
