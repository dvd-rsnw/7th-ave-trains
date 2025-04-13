from typing import List, Dict
from fastapi import APIRouter
import time
from google.transit import gtfs_realtime_pb2
import httpx
from train_types import TrainArrival, FeedEntity, DirectionalTrainArrival
from .raw_feed_g import raw_feed_g

router = APIRouter()

QUEENS_BOUND_STOP_ID = "F24N"
BROOKLYN_BOUND_STOP_ID = "F24S"
MIN_MINUTES_THRESHOLD = 3

feed = gtfs_realtime_pb2.FeedMessage()

@router.get("/g-train", response_model=List[TrainArrival])
def g_train_times(direction: str = "both", min_threshold: int = MIN_MINUTES_THRESHOLD):
    response = httpx.get("https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g")
    feed.ParseFromString(response.content)
    
    arrivals = []

    for entity in feed.entity:
        if entity.HasField('trip_update'):
            trip_update = entity.trip_update
            for stop_time_update in trip_update.stop_time_update:
                stop_id = stop_time_update.stop_id
                stop_ids = [QUEENS_BOUND_STOP_ID, BROOKLYN_BOUND_STOP_ID]
                if (direction == "queens"):
                    stop_ids = [QUEENS_BOUND_STOP_ID]
                elif (direction == "brooklyn"):
                    stop_ids = [BROOKLYN_BOUND_STOP_ID]

                if stop_id in stop_ids:
                    if stop_time_update.HasField('arrival'):
                        arrival_time = stop_time_update.arrival.time
                        time_until = arrival_time - int(time.time())
                        minutes_until = time_until // 60
                        
                        if minutes_until < min_threshold:
                            continue
                        
                        train_direction = "queens" if stop_id.endswith("N") else "brooklyn"
                        status = f"{minutes_until} min{'s' if minutes_until != 1 else ''}"
                            
                        arrivals.append(TrainArrival(
                            direction=train_direction,
                            minutes_until=minutes_until,
                            status=status,
                            express=False  # G trains are always local
                        ))
    
    return arrivals

@router.get("/g-train-raw", response_model=Dict[str, List[FeedEntity]])
def g_train_raw():
    return raw_feed_g()

@router.get("/g-train-queens", response_model=List[DirectionalTrainArrival])
def g_train_queens():
    arrivals = g_train_times("queens")
    return [DirectionalTrainArrival(status=arr.status, express=False, line="G") for arr in arrivals]

@router.get("/g-train-queens-next", response_model=List[DirectionalTrainArrival])
def g_train_next_queens():
    arrivals = g_train_times("queens", min_threshold=MIN_MINUTES_THRESHOLD)
    return [DirectionalTrainArrival(status=arr.status, express=False, line="G") for arr in arrivals][:2]

@router.get("/g-train-brooklyn", response_model=List[DirectionalTrainArrival])
def g_train_brooklyn():
    arrivals = g_train_times("brooklyn")
    return [DirectionalTrainArrival(status=arr.status, express=False, line="G") for arr in arrivals]

@router.get("/g-train-brooklyn-next", response_model=List[DirectionalTrainArrival])
def g_train_next_brooklyn():
    arrivals = g_train_times("brooklyn", min_threshold=MIN_MINUTES_THRESHOLD)
    return [DirectionalTrainArrival(status=arr.status, express=False, line="G") for arr in arrivals][:2] 