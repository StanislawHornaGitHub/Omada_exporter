from pydantic import BaseModel, Field


class ApWirelessUpLink(BaseModel):
    uplinkMac: str
    name: str
    channel: int
    rssi: int
    snr: int
    txRate: str
    rxRateInt: int
    rxRate: str
    upBytes: int
    downBytes: int
    upPackets: int
    downPackets: int
    activity: int
