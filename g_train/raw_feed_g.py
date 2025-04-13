from google.transit import gtfs_realtime_pb2
import httpx
from train_types import FeedEntity
import time

feed = gtfs_realtime_pb2.FeedMessage()

def raw_feed_g():
    response = httpx.get("https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g", headers=headers)
    feed.ParseFromString(response.content)
    
    current_time = int(time.time())
    one_minute_future = current_time + 60
    target_stops = {'F24N', 'F24S'}
    
    entities = []
    for entity in feed.entity:
        # Skip if there's no trip update or it's marked as deleted
        if not entity.HasField('trip_update') or entity.is_deleted:
            continue
            
        # Check if any stop time updates have future arrivals at our target stops
        trip_update = entity.trip_update
        has_future_target_stop = False
        if trip_update.stop_time_update:
            for stu in trip_update.stop_time_update:
                if (stu.HasField('stop_id') and 
                    stu.stop_id in target_stops and
                    stu.HasField('arrival') and 
                    stu.arrival.HasField('time') and 
                    stu.arrival.time > one_minute_future):
                    has_future_target_stop = True
                    break
        
        if not has_future_target_stop:
            continue
            
        feed_entity = {
            "id": entity.id,
            "is_deleted": entity.is_deleted if entity.HasField('is_deleted') else None,
            "trip_update": None,
            "vehicle": None,
            "alert": None
        }
        
        if entity.HasField('trip_update'):
            trip_update = entity.trip_update
            feed_entity["trip_update"] = {
                "trip": {
                    "trip_id": trip_update.trip.trip_id if trip_update.trip.HasField('trip_id') else None,
                    "route_id": trip_update.trip.route_id if trip_update.trip.HasField('route_id') else None,
                    "direction_id": trip_update.trip.direction_id if trip_update.trip.HasField('direction_id') else None,
                    "start_time": trip_update.trip.start_time if trip_update.trip.HasField('start_time') else None,
                    "start_date": trip_update.trip.start_date if trip_update.trip.HasField('start_date') else None,
                    "schedule_relationship": trip_update.trip.schedule_relationship if trip_update.trip.HasField('schedule_relationship') else None
                },
                "vehicle": {
                    "id": trip_update.vehicle.id if trip_update.HasField('vehicle') and trip_update.vehicle.HasField('id') else None,
                    "label": trip_update.vehicle.label if trip_update.HasField('vehicle') and trip_update.vehicle.HasField('label') else None,
                    "license_plate": trip_update.vehicle.license_plate if trip_update.HasField('vehicle') and trip_update.vehicle.HasField('license_plate') else None
                } if trip_update.HasField('vehicle') else None,
                "stop_time_update": [{
                    "stop_sequence": stu.stop_sequence if stu.HasField('stop_sequence') else None,
                    "stop_id": stu.stop_id if stu.HasField('stop_id') else None,
                    "arrival": {
                        "delay": stu.arrival.delay if stu.arrival.HasField('delay') else None,
                        "time": stu.arrival.time if stu.arrival.HasField('time') else None,
                        "uncertainty": stu.arrival.uncertainty if stu.arrival.HasField('uncertainty') else None
                    } if stu.HasField('arrival') else None,
                    "departure": {
                        "delay": stu.departure.delay if stu.departure.HasField('delay') else None,
                        "time": stu.departure.time if stu.departure.HasField('time') else None,
                        "uncertainty": stu.departure.uncertainty if stu.departure.HasField('uncertainty') else None
                    } if stu.HasField('departure') else None,
                    "schedule_relationship": stu.schedule_relationship if stu.HasField('schedule_relationship') else None
                } for stu in trip_update.stop_time_update] if trip_update.stop_time_update else None,
                "timestamp": trip_update.timestamp if trip_update.HasField('timestamp') else None,
                "delay": trip_update.delay if trip_update.HasField('delay') else None
            }
        
        if entity.HasField('vehicle'):
            vehicle = entity.vehicle
            feed_entity["vehicle"] = {
                "trip": {
                    "trip_id": vehicle.trip.trip_id if vehicle.trip.HasField('trip_id') else None,
                    "route_id": vehicle.trip.route_id if vehicle.trip.HasField('route_id') else None,
                    "direction_id": vehicle.trip.direction_id if vehicle.trip.HasField('direction_id') else None,
                    "start_time": vehicle.trip.start_time if vehicle.trip.HasField('start_time') else None,
                    "start_date": vehicle.trip.start_date if vehicle.trip.HasField('start_date') else None,
                    "schedule_relationship": vehicle.trip.schedule_relationship if vehicle.trip.HasField('schedule_relationship') else None
                } if vehicle.HasField('trip') else None,
                "vehicle": {
                    "id": vehicle.vehicle.id if vehicle.vehicle.HasField('id') else None,
                    "label": vehicle.vehicle.label if vehicle.vehicle.HasField('label') else None,
                    "license_plate": vehicle.vehicle.license_plate if vehicle.vehicle.HasField('license_plate') else None
                } if vehicle.HasField('vehicle') else None,
                "position": {
                    "latitude": vehicle.position.latitude if vehicle.position.HasField('latitude') else None,
                    "longitude": vehicle.position.longitude if vehicle.position.HasField('longitude') else None,
                    "bearing": vehicle.position.bearing if vehicle.position.HasField('bearing') else None,
                    "odometer": vehicle.position.odometer if vehicle.position.HasField('odometer') else None,
                    "speed": vehicle.position.speed if vehicle.position.HasField('speed') else None
                } if vehicle.HasField('position') else None,
                "current_stop_sequence": vehicle.current_stop_sequence if vehicle.HasField('current_stop_sequence') else None,
                "stop_id": vehicle.stop_id if vehicle.HasField('stop_id') else None,
                "current_status": vehicle.current_status if vehicle.HasField('current_status') else None,
                "timestamp": vehicle.timestamp if vehicle.HasField('timestamp') else None,
                "congestion_level": vehicle.congestion_level if vehicle.HasField('congestion_level') else None,
                "occupancy_status": vehicle.occupancy_status if vehicle.HasField('occupancy_status') else None
            }
            
        if entity.HasField('alert'):
            alert = entity.alert
            feed_entity["alert"] = {
                "active_period": [{
                    "start": period.start if period.HasField('start') else None,
                    "end": period.end if period.HasField('end') else None
                } for period in alert.active_period] if alert.active_period else None,
                "informed_entity": [{
                    "agency_id": entity.agency_id if entity.HasField('agency_id') else None,
                    "route_id": entity.route_id if entity.HasField('route_id') else None,
                    "route_type": entity.route_type if entity.HasField('route_type') else None,
                    "trip": {
                        "trip_id": entity.trip.trip_id if entity.trip.HasField('trip_id') else None,
                        "route_id": entity.trip.route_id if entity.trip.HasField('route_id') else None,
                        "direction_id": entity.trip.direction_id if entity.trip.HasField('direction_id') else None,
                        "start_time": entity.trip.start_time if entity.trip.HasField('start_time') else None,
                        "start_date": entity.trip.start_date if entity.trip.HasField('start_date') else None,
                        "schedule_relationship": entity.trip.schedule_relationship if entity.trip.HasField('schedule_relationship') else None
                    } if entity.HasField('trip') else None,
                    "stop_id": entity.stop_id if entity.HasField('stop_id') else None
                } for entity in alert.informed_entity] if alert.informed_entity else None,
                "cause": alert.cause if alert.HasField('cause') else None,
                "effect": alert.effect if alert.HasField('effect') else None,
                "url": {
                    "text": alert.url.text if alert.url.HasField('text') else None,
                    "language": alert.url.language if alert.url.HasField('language') else None
                } if alert.HasField('url') else None,
                "header_text": {
                    "text": alert.header_text.text if alert.header_text.HasField('text') else None,
                    "language": alert.header_text.language if alert.header_text.HasField('language') else None
                } if alert.HasField('header_text') else None,
                "description_text": {
                    "text": alert.description_text.text if alert.description_text.HasField('text') else None,
                    "language": alert.description_text.language if alert.description_text.HasField('language') else None
                } if alert.HasField('description_text') else None
            }
            
        entities.append(FeedEntity(**feed_entity))
    
    return entities 