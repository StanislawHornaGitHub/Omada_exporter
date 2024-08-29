from pydantic import BaseModel, Field

class SwitchPortStats(BaseModel):
    name: str = Field(alias="switchName")
    mac: str = Field(alias="switchMac")
    port: int
    tx: int
    rx: int
    txRate: int
    rxRate: int
    txPkts: int
    rxPkts: int
    txBroadPkts: int
    rxBroadPkts: int
    txMultiPkts: int
    rxMultiPkts: int
    dropPkts: int
    txErrPkts: int
    rxErrPkts: int
    
    
    