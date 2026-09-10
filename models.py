from sqlalchemy import Column, Integer, Float, String, DateTime, UniqueConstraint
from database import Base


class Rainfall(Base):
    __tablename__ = "rainfall"

    __table_args__ = (
    UniqueConstraint("latitude", "longitude", "timestamp"),
)
  

    id = Column(Integer, primary_key=True,index=True)
    latitude= Column(Float)
    longitude = Column(Float)
    timestamp = Column(DateTime)
    precipitation = Column(Float)
    unit = Column(String)
    risk_level=Column(String)
    risk_score=Column(Float)
    


class SoilMoisture(Base):
    __tablename__="soil_moisture"

    id=Column(Integer,primary_key=True,index=True)
    latitude=Column(Float)
    longitude=Column(Float)
    timestamp=Column(DateTime)
    moisture=Column(Float)
    unit = Column(String)