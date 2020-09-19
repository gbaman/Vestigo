
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, BigInteger, Time, Boolean, text, Enum
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///vestigo.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()
metadata = Base.metadata


class DataEntry(Base):
    __tablename__ = 'data_entries'
    data_entry_id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    sensor_name = Column(String(45), nullable=False)
    sensor_value = Column(Integer, nullable=False)
    data_entry_date_time = Column(DateTime, nullable=False)
    data_entry_uploaded = Column(Boolean, nullable=False)
