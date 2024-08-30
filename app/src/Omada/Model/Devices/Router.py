from pydantic import BaseModel, Field, field_serializer
import datetime
import src.Omada.helpers.timeFunctions as timeHelpers

from src.Omada.Model.subModels.RouterPort import RouterPort

class Router(BaseModel):
    deviceType: str = Field(default="Router")
    name: str
    mac: str 
    model: str = Field(alias="showModel")
    firmwareVersion: str
    ip: str
    uptime: str
    temp: int
    cpuUtil: int
    memUtil: int
    ipv6List: list[str] = Field(default=None)
    lastSeen: datetime.datetime
    portConfigs: list[RouterPort]
    
    
    def __init__(self, **data):
        
        data["lastSeen"] = timeHelpers.get_last_seen(data["lastSeen"])
        
        super().__init__(**data)
    
    @field_serializer('lastSeen')
    def serialize_lastSeen(self, lastSeen: datetime.datetime, _info) -> str:
        return timeHelpers.datetime_to_string(lastSeen)