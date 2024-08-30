from pydantic import BaseModel, Field


class ApRadioConfig(BaseModel):
    name: str
    mac: str
    frequency: str
    actualChannel: str
    maxTxRate: str
    region: str
    bandWidth: str
    mode: str = Field(alias="rdMode")
    txUtil: int
    rxUtil: int
    interUtil: int

    def __init__(self, **data):
        data["maxTxRate"] = str(data["maxTxRate"])
        data["region"] = str(data["region"])

        super().__init__(**data)
