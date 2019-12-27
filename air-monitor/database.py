from typing import List

from models import *
import datetime

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    Base.metadata.create_all(bind=engine)

    
init_db()


def get_node_from_node_key(node_key):
    node = db_session.query(Node).filter(Node.node_key == node_key).first()
    return node


def add_data(node:Node, data_key, data_value):
    data = DataEntry(node_id=node.node_id, data_entry_date_time=datetime.datetime.now(), data_entry_key=data_key, data_entry_value=data_value)
    db_session.add(data)
    db_session.commit()


def get_data_by_node_id_key(node_id, data_key) -> List[DataEntry]:
    data = db_session.query(DataEntry).filter(DataEntry.node_id == node_id, DataEntry.data_entry_key == data_key).all()
    return data