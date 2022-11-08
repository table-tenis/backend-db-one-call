""" Python Script Comprise 
    Mariadb Connector And
    Kafka Consumer To Topic1, Topic2.
    --------------------------------
    Detection And MOT Data Will Be 
    Consumed From Kafka Server 
    And Then Insert Into Mariadb Server.
"""


from json import loads
from datetime import datetime
import time
import sqlalchemy
from sqlalchemy import create_engine, Integer, String, Column, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select
from pydantic import parse_raw_as
from pydantic.error_wrappers import ValidationError
from confluent_kafka import Consumer
from data_schema import Topic1Model, Topic2Model
from config.config import settings
import helper

TOPIC1 = "RawMotMeta"
TOPIC2 = 'RawFaceMeta'
TOPIC100 = 'HDImage'

MARIADB_URL = f"mysql+pymysql://{settings.MARIADB_USERNAME}:{settings.MARIADB_PASSWORD}@{settings.MARIADB_HOST}:{settings.MARIADB_PORT}/{settings.MARIADB_DB_NAME}"
print("MARIADB_URL = ", MARIADB_URL)
engine = create_engine(MARIADB_URL + '?charset=utf8', echo=True)
Base = declarative_base(engine)

class Detection(Base):
    __tablename__ = 'detection'
    __table_args__ = {'autoload': True}
    
class Mot(Base):
    __tablename__ = 'mot'
    __table_args__ = {'autoload': True}
    
class Staff(Base):
    __tablename__ = 'staff'
    __table_args__ = {'autoload': True}
    
class Camera(Base):
    __tablename__ = 'camera'
    __table_args__ = {'autoload': True}


KAFKA_SERVER_URL = f"{settings.KAFKA_SERVER_HOST}:{settings.KAFKA_SERVER_PORT}"
print("KAFKA_SERVER_URL = ", KAFKA_SERVER_URL, ", KAFKA_CONSUMER_GROUP_ID = ", settings.KAFKA_CONSUMER_GROUP_ID)
consumer = Consumer({
    'bootstrap.servers': KAFKA_SERVER_URL,
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': 'true',
    'auto.commit.interval.ms': 1000,
    # 'session.timeout.ms': 900000,
    # 'heartbeat.interval.ms': 15000,
    'group.id': settings.KAFKA_CONSUMER_GROUP_ID
})
Session = sqlalchemy.orm.sessionmaker(bind=engine)
SESSION = Session()

consumer.subscribe([TOPIC1, TOPIC2])

index = 0
    
list_detect = []  
list_mot = []
old_time = ""
new_time = ""
while True:
    start_time = time.time()
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print(f"Consumer error: {msg.error()}")
        continue

    try:
        data = loads(msg.value())
        if "face" in data:
            # print("==================> Decode facedata")
            payload = parse_raw_as(Topic2Model, msg.value())
            staff = SESSION.execute(select(Staff).where(Staff.staff_code == payload.face.staff_id)).first()
            camera = SESSION.execute(select(Camera).where(Camera.id == payload.camera_id)).first()
            if staff and camera:
                # print(staff[0].id, staff[0].staff_code, staff[0].fullname)
                # camera = SESSION.execute(select(Camera).where(Camera.ip == data['ip'])).first()
                staff = staff[0]
                # print("=====================> (staff_id, staff_code, fullname) = ", staff.id, staff.staff_code, staff.fullname)
                camera = camera[0]
                x, y, w, h = payload.face.bbox.x, payload.face.bbox.y, payload.face.bbox.w, payload.face.bbox.h
                polygon = f"POLYGON(({x} {y},{x+w} {y},{x+w} {y+h},{x} {y+h},{x} {y}))"
                insert_data = {'staff_id':staff.id, 'cam_id':payload.camera_id, 'session_id':payload.session_id,
                        'frame_id': payload.frame_id, 'detection_time':helper.datetime_to_str(helper.datetime_from_utc_to_local(payload.srctime)), 
                        'detection_score': payload.face.score, 'box_x':payload.face.bbox.x, 'box_y': payload.face.bbox.y, 
                        'box_width':payload.face.bbox.w, 'box_height':payload.face.bbox.h, 'feature': payload.face.feature,
                        'polygon_face': polygon}
                list_detect.append(insert_data)
                if(len(list_detect) >= 100):
                    try:
                        SESSION.execute(Detection.__table__.insert(), list_detect)
                        SESSION.commit()
                        insert_time = (time.time() - start_time)*1000.0
                        print("==================== insert-time = ", insert_time, " milliseconds")
                        list_detect.clear()
                    except Exception as e:
                        SESSION.rollback()
                        print("===============> [MARIADB ERROR]: ", e._message())
                
        elif "MOT" in data:
            # print("==================> Decode motdata")
            payload = parse_raw_as(Topic1Model, msg.value())
            camera = SESSION.execute(select(Camera).where(Camera.id == payload.camera_id)).first()
            if camera:
                for mot in payload.MOT:
                    x, y, w, h = mot.bbox.x, mot.bbox.y, mot.bbox.w, mot.bbox.h
                    polygon = f"POLYGON(({x} {y},{x+w} {y},{x+w} {y+h},{x} {y+h},{x} {y}))"
                    insert_data = {'cam_id':payload.camera_id, 'session_id':payload.session_id,
                            'frame_id': payload.frame_id, 'track_time':helper.datetime_to_str(helper.datetime_from_utc_to_local(payload.srctime)), 
                            'track_id': mot.object_id,
                            'box_x':mot.bbox.x, 'box_y': mot.bbox.y, 'box_width':mot.bbox.w, 'box_height':mot.bbox.h,
                            'polygon_shape': polygon}
                    list_mot.append(insert_data)
                if(len(list_mot) >= 100):
                    try:
                        SESSION.execute(Mot.__table__.insert(), list_mot)
                        SESSION.commit()
                        insert_time = (time.time() - start_time)*1000.0
                        print("==================== insert-time = ", insert_time, " milliseconds")
                        list_mot.clear()
                    except Exception as e:
                        SESSION.rollback()
                        print("===============> [MARIADB ERROR]: ", e._message())
        
    except ValueError as e:
        print('===============> [CONSUMER ERROR]: ', str(e), end='')

consumer.close()