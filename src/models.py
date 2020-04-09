#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from contextlib import contextmanager

import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("sqlite:///local.db", echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
@contextmanager
def db_session():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

class Region(Enum):
    APAC = 1
    EMEA = 2
    IND = 3
    LATAM = 4
    NA = 5
    Mobile = 6


class Sites(Base):
    __tablename__ = "sites"
    id = Column(String, primary_key=True)
    lat = Column(Integer)
    lon = Column(Integer)
    rc_ext = Column(Integer)
    country = Column(String)
    region = Column(Region)
    locations = relationship("LocationMap", uselist=True, back_populates="site")
    exts = relationship("Exts", uselist=True, back_populates="site")
    
    def repr(self):
        return f'<Sites(site={site}, did_id={did_id}, lat={lat}, lon={lon}, rc_ext={rc_ext}, country={country}, region={region}, )>'
    __repr__ = repr


class Exts(Base):
    __tablename__ = "exts"
    id = Column(Integer, primary_key=True)
    site_id = Column(String, ForeignKey("sites.id"))
    site = relationship("Sites", back_populates="exts")
    mask = Column(Integer)
    prefix = Column(Integer)
    start = Column(Integer)
    end = Column(Integer)

    def repr(self):
        return f'<Exts(id={id}, site={site}, mask={mask}, prefix={prefix}, start={start},end={end}, )>'
    __repr__ = repr


class LocationMap(Base):
    __tablename__ = "loc_map"
    id = Column(String, primary_key=True)
    site_id = Column(String, ForeignKey("sites.id"))
    site = relationship("Sites", back_populates="locations")

    def repr(self):
        return f'<LocationMap(id={id}, site={site}, )>'
    __repr__ = repr


Base.metadata.create_all(engine)

def get_class_by_tablename(name):
    for c in Base._decl_class_registry.values():
        if hasattr(c, '__tablename__'):
            if c.__tablename__ == name: 
                return c
