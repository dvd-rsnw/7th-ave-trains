from typing import List, Dict
from fastapi import APIRouter
import time
from google.transit import gtfs_realtime_pb2
import httpx
from train_types import TrainArrival, FeedEntity, DirectionalTrainArrival
from .raw_feed_f import raw_feed_f

router = APIRouter()

MANHATTAN_BOUND_STOP_ID = "F24N"
BROOKLYN_BOUND_STOP_ID = "F24S"
FOUR_AV_MANHATTAN_BOUND_STOP_ID = "F23N"
FOUR_AV_BROOKLYN_BOUND_STOP_ID = "F23S"
MIN_MINUTES_THRESHOLD = 3

feed = gtfs_realtime_pb2.FeedMessage()

@router.get("/f-train", response_model=List[TrainArrival])
def f_train_times(direction: str = "both", min_threshold: int = MIN_MINUTES_THRESHOLD):
    response = httpx.get("https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm")
    feed.ParseFromString(response.content)
    
    arrivals = []

    for entity in feed.entity:
        if entity.HasField('trip_update'):
            trip_update = entity.trip_update
            # Check if this train stops at 4th Avenue
            stops_at_four_av = False
            for stop in trip_update.stop_time_update:
                if stop.stop_id in [FOUR_AV_MANHATTAN_BOUND_STOP_ID, FOUR_AV_BROOKLYN_BOUND_STOP_ID]:
                    stops_at_four_av = True
                    break

            for stop_time_update in trip_update.stop_time_update:   
                stop_id = stop_time_update.stop_id
                stop_ids = [MANHATTAN_BOUND_STOP_ID, BROOKLYN_BOUND_STOP_ID]
                if (direction == "manhattan"):
                    stop_ids = [MANHATTAN_BOUND_STOP_ID]
                elif (direction == "brooklyn"):
                    stop_ids = [BROOKLYN_BOUND_STOP_ID]

                if stop_id in stop_ids:
                    if stop_time_update.HasField('arrival'):
                        arrival_time = stop_time_update.arrival.time
                        time_until = arrival_time - int(time.time())
                        minutes_until = time_until // 60
                        
                        # Skip trains that have departed or are less than min_threshold minutes away
                        if minutes_until < min_threshold:
                            continue
                        
                        train_direction = "manhattan" if stop_id.endswith("N") else "brooklyn"
                        status = f"{minutes_until} min{'s' if minutes_until != 1 else ''}"
                            
                        arrivals.append(TrainArrival(
                            direction=train_direction,
                            minutes_until=minutes_until,
                            status=status,
                            express=not stops_at_four_av
                        ))
    
    return arrivals

@router.get("/f-train-raw", response_model=Dict[str, List[FeedEntity]])
def f_train_raw():
    return raw_feed_f()

@router.get("/f-train-manhattan", response_model=List[DirectionalTrainArrival])
def f_train_manhattan():
    arrivals = f_train_times(direction="manhattan")
    return [DirectionalTrainArrival(status=arr.status, express=arr.express, line="F") for arr in arrivals]

@router.get("/f-train-manhattan-next", response_model=List[DirectionalTrainArrival])
def f_train_manhattan_next():
    arrivals = f_train_times(direction="manhattan", min_threshold=MIN_MINUTES_THRESHOLD)
    return [DirectionalTrainArrival(status=arr.status, express=arr.express, line="F") for arr in arrivals][:2]

@router.get("/f-train-brooklyn", response_model=List[DirectionalTrainArrival])
def f_train_brooklyn():
    arrivals = f_train_times(direction="brooklyn")
    return [DirectionalTrainArrival(status=arr.status, express=arr.express, line="F") for arr in arrivals]

@router.get("/f-train-brooklyn-next", response_model=List[DirectionalTrainArrival])
def f_train_brooklyn_next():
    arrivals = f_train_times(direction="brooklyn", min_threshold=MIN_MINUTES_THRESHOLD)
    return [DirectionalTrainArrival(status=arr.status, express=arr.express, line="F") for arr in arrivals][:2] 