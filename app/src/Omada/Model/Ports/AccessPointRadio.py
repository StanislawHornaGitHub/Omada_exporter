from pydantic import BaseModel, Field
from src.Omada.Model.subModels.ApRadioConfig import ApRadioConfig
from src.Omada.Model.subModels.ApRadioTraffic import ApRadioTraffic


class AccessPointRadio(BaseModel):
    name: str = Field(alias="accessPointName")
    mac: str = Field(alias="accessPointMac")
    radioTraffic24GHz: ApRadioTraffic = Field(alias="radioTraffic2g")
    radioTraffic50GHz: ApRadioTraffic = Field(alias="radioTraffic5g")
    radioConfig24GHz: ApRadioConfig = Field(alias="wp2g")
    radioConfig50GHz: ApRadioConfig = Field(alias="wp5g")

    def __init__(self, **data):
        data["radioTraffic2g"]["frequency"] = "2.4 GHz"
        data["radioTraffic2g"]["mac"] = data["accessPointMac"]
        data["radioTraffic2g"]["name"] = data["accessPointName"]
        data["radioTraffic5g"]["frequency"] = "5 GHz"
        data["radioTraffic5g"]["mac"] = data["accessPointMac"]
        data["radioTraffic5g"]["name"] = data["accessPointName"]
        data["wp2g"]["frequency"] = "2.4 GHz"
        data["wp2g"]["mac"] = data["accessPointMac"]
        data["wp2g"]["name"] = data["accessPointName"]
        data["wp5g"]["frequency"] = "5 GHz"
        data["wp5g"]["mac"] = data["accessPointMac"]
        data["wp5g"]["name"] = data["accessPointName"]
        super().__init__(**data)
