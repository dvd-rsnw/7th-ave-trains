from typing import List, Optional
from pydantic import BaseModel

class TrainArrival(BaseModel):
    direction: str
    minutes_until: int
    status: str
    express: bool = False

class DirectionalTrainArrival(BaseModel):
    status: str
    express: bool = False
    line: str

class StopTimeEvent(BaseModel):
    delay: Optional[int] = None
    time: Optional[int] = None
    uncertainty: Optional[int] = None

class StopTimeUpdate(BaseModel):
    stop_sequence: Optional[int] = None
    stop_id: Optional[str] = None
    arrival: Optional[StopTimeEvent] = None
    departure: Optional[StopTimeEvent] = None
    schedule_relationship: Optional[int] = None

class TripDescriptor(BaseModel):
    trip_id: Optional[str] = None
    route_id: Optional[str] = None
    direction_id: Optional[int] = None
    start_time: Optional[str] = None
    start_date: Optional[str] = None
    schedule_relationship: Optional[int] = None

class VehicleDescriptor(BaseModel):
    id: Optional[str] = None
    label: Optional[str] = None
    license_plate: Optional[str] = None

class Position(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    bearing: Optional[float] = None
    odometer: Optional[float] = None
    speed: Optional[float] = None

class VehiclePosition(BaseModel):
    trip: Optional[TripDescriptor] = None
    vehicle: Optional[VehicleDescriptor] = None
    position: Optional[Position] = None
    current_stop_sequence: Optional[int] = None
    stop_id: Optional[str] = None
    current_status: Optional[int] = None
    timestamp: Optional[int] = None
    congestion_level: Optional[int] = None
    occupancy_status: Optional[int] = None

class TimeRange(BaseModel):
    start: Optional[int] = None
    end: Optional[int] = None

class TranslatedString(BaseModel):
    text: Optional[str] = None
    language: Optional[str] = None

class EntitySelector(BaseModel):
    agency_id: Optional[str] = None
    route_id: Optional[str] = None
    route_type: Optional[int] = None
    trip: Optional[TripDescriptor] = None
    stop_id: Optional[str] = None

class Alert(BaseModel):
    active_period: Optional[List[TimeRange]] = None
    informed_entity: Optional[List[EntitySelector]] = None
    cause: Optional[int] = None
    effect: Optional[int] = None
    url: Optional[TranslatedString] = None
    header_text: Optional[TranslatedString] = None
    description_text: Optional[TranslatedString] = None

class TripUpdate(BaseModel):
    trip: Optional[TripDescriptor] = None
    vehicle: Optional[VehicleDescriptor] = None
    stop_time_update: Optional[List[StopTimeUpdate]] = None
    timestamp: Optional[int] = None
    delay: Optional[int] = None

class FeedEntity(BaseModel):
    id: str
    is_deleted: Optional[bool] = None
    trip_update: Optional[TripUpdate] = None
    vehicle: Optional[VehiclePosition] = None
    alert: Optional[Alert] = None 