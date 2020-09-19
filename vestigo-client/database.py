from typing import List
import logging

from models import *
import datetime


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    Base.metadata.create_all(bind=engine)


init_db()


def mark_uploaded(record:DataEntry):
    record.data_entry_uploaded = True
    db_session.commit()


def add_data_entry(sensor_name, sensor_value, date_time, uploaded):
    data = DataEntry(sensor_name=sensor_name, sensor_value=sensor_value, data_entry_date_time=date_time, data_entry_uploaded=uploaded)
    db_session.add(data)
    db_session.commit()
    return data


def get_all_unuploaded():
    entries = db_session.query(DataEntry).filter(DataEntry.data_entry_uploaded == False)
    return entries.all()