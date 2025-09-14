from sqlalchemy import Column, Integer, String, TIMESTAMP, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Trips(Base):
    __tablename__ = "trips"

    trip_id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, nullable=False)
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP, nullable=False)
    start_lat = Column(Float, nullable=False)
    start_lon = Column(Float, nullable=False)
    end_lat = Column(Float, nullable=False)
    end_lon = Column(Float, nullable=False)
    distance_miles = Column(Float, nullable=False)
    duration = Column(Float, nullable=False)
    avg_speed = Column(Float, nullable=False)
    max_speed = Column(Float, nullable=False)
    hard_brakes = Column(Integer, nullable=False)
    time_of_day = Column(String(10), nullable=False)
    weather = Column(String(20), nullable=False)
