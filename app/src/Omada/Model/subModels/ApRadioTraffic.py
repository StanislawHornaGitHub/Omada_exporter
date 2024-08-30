from pydantic import BaseModel, Field


class ApRadioTraffic(BaseModel):
    name: str
    mac: str
    frequency: str
    rxPkts: int
    txPkts: int
    rx: int
    tx: int
    rxDropPkts: int
    txDropPkts: int
    rxErrPkts: int
    txErrPkts: int
    rxRetryPkts: int
    txRetryPkts: int
