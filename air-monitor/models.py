
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, BigInteger, Time, Boolean, text, Enum
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from secrets.config import db_user, db_pass, db_name, db_host


engine = create_engine('mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(db_user, db_pass, db_host, db_name))
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()
metadata = Base.metadata


class Node(Base):
    __tablename__ = 'nodes'

    node_id = Column(Integer, primary_key=True, unique=True)
    node_name = Column(String(45))
    node_key = Column(String(45))


class DataEntry(Base):
    __tablename__ = 'data_entries'

    data_entry_id = Column(Integer, primary_key=True, unique=True)
    node_id = Column(ForeignKey('nodes.node_id'), primary_key=True, nullable=False, index=True)
    data_entry_date_time = Column(DateTime, nullable=False)
    data_entry_key = Column(String(45))
    data_entry_value = Column(String(45))