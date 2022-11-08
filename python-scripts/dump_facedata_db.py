import pandas as pd 
import numpy as np
from datetime import date, datetime

from datetime import datetime
import sqlalchemy
from sqlalchemy import create_engine, Integer, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker, Session
from config.config import settings

MARIADB_URL = f"mysql+pymysql://{settings.MARIADB_USERNAME}:{settings.MARIADB_PASSWORD}@{settings.MARIADB_HOST}:{settings.MARIADB_PORT}/{settings.MARIADB_DB_NAME}"
print("MARIADB_URL = ", MARIADB_URL)
engine = create_engine(MARIADB_URL + '?charset=utf8', echo=True)
Base = declarative_base(engine)

class Enterprise(Base):
    __tablename__ = 'enterprise'
    __table_args__ = {'autoload': True}
    
class Staff(Base):
    __tablename__ = 'staff'
    __table_args__ = {'autoload': True}
    
class Site(Base):
    __tablename__ = 'site'
    __table_args__ = {'autoload': True}
    
class FaceID(Base):
    __tablename__ = 'faceid'
    __table_args__ = {'autoload': True}
    
class ShiftTime(Base):
    __tablename__ = 'shift_time'
    __table_args__ = {'autoload': True}
    
class ShiftRegister(Base):
    __tablename__ = 'shift_register'
    staff_id = Column(Integer, primary_key=True)
    shift_type = Column(String, primary_key=True)
    weekday = Column(Integer, primary_key=True)
    
class SiteIORegister(Base):
    __tablename__ = 'site_io_register'
    __table_args__ = {'autoload': True}
    
class Camera(Base):
    __tablename__ = 'camera'
    __table_args__ = {'autoload': True}

# class RestrictedROI(Base):
#     __tablename__ = 'restricted_roi'
#     __table_args__ = {'autoload': True}

class Detection(Base):
    __tablename__ = 'detection'
    __table_args__ = {'autoload': True}
    
class MOT(Base):
    __tablename__ = 'mot'
    __table_args__ = {'autoload': True}
    
class MTAR(Base):
    __tablename__ = 'mtar'
    __table_args__ = {'autoload': True}

NUM_RECEIVED_PACKET = 0
NUM_INSERTED = 0

def dump_staff_data():
    df = pd.read_csv('dump-data/staff2.csv', dtype={"cellphone": str})
    df = df.where(pd.notnull(df), None)
    list_staff = []
    with Session(engine) as session:
        staffs = session.execute(select(Staff)).all()
        if not staffs:
            for idx in df.index:
                state = 1
                if df['activate'][idx] == False:
                    state = 0
                list_staff.append({'staff_code':df['staff_code'][idx], 'fullname':df['full_name'][idx],
                                'email_code':df['mail_code'][idx], 'cellphone':df['cellphone'][idx], 'unit':df['unit'][idx],
                                'title':df['title'][idx], 'date_of_birth':df['date_of_birth'][idx],
                                'sex': df['sex'][idx], 'note':df['note'][idx],
                                'notify_enable':df['should_diemdanh'][idx], 'state':state})
            session.execute(Staff.__table__.insert(), list_staff)
            session.commit()
        else:
            print("Database has staff records")
    
def update_staff_data():
    df = pd.read_csv('dump-data/staff2.csv', dtype={"cellphone": str})
    df = df.where(pd.notnull(df), None)
    list_staff = []
    with Session(engine) as session:
        for idx in df.index:
            if df['activate'][idx] == False:
                print(df['staff_code'][idx], df['full_name'][idx], df['activate'][idx]) 
                staff = session.execute(select(Staff).where(Staff.staff_code == df['staff_code'][idx])).first()
                staff[0].state = 0
                session.add(staff[0])
                session.commit()
    
def dump_site_data():
    with Session(engine) as session:
        dump = Site(enterprise_id=1, name="Xuong X1", description="Xuong X1 located in Hoa Lac")
        session.add(dump)
        session.commit()
 
def datetime_to_str(date_obj):
    if(date_obj == None or (isinstance(date_obj, datetime) == False)):
      return None
    try:
      return datetime.strftime(date_obj, '%Y-%m-%d %H:%M:%S.%f')
    except ValueError as err:
      print('ValueError: ', err) 
    
def dump_camera_data():
    df = pd.read_csv('dump-data/camera.csv', dtype={"floor": int})
    list_camera = []
    for idx in df.index:
        list_camera.append({'site_id':1, 'session_service_id':1, 'ip':df['ip'][idx],
                           'description':"camera tang " + str(df['floor'][idx])})
    with Session(engine) as session:
        session.execute(Camera.__table__.insert(), list_camera)
        session.commit()
    
def get_staff():
    with Session(engine) as session:
        staffs = session.execute(select(Staff).where(Staff.staff_code == '015234')).all()
        for staff in staffs:
            print(staff[0].id, staff[0].staff_code, staff[0].fullname)

if __name__ == "__main__":
    # dump_enterprise_data()
    dump_staff_data()
    # dump_site_data()
    # dump_session_service_data()
    # dump_camera_data()