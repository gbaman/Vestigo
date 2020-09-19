import datetime
import requests
import logging

from . import database


class Vestigo():
    def __init__(self, url, node_key):
        self.base_url = url
        self.node_key = node_key

    def log_sensor(self, sensor_name, sensor_value, upload=True):
        database_entry = database.add_data_entry(sensor_name, sensor_value, datetime.datetime.now(), uploaded=False)
        if upload:
            upload_success = self._upload_entry(database_entry)
            if upload_success:
                database.mark_uploaded(database_entry)
                unuploaded_entries = database.get_all_unuploaded()
                if unuploaded_entries:
                    logging.info(f"Connection to server reestablished, uploading {len(unuploaded_entries)} entries.")
                    for entry in unuploaded_entries:
                        if self._upload_entry(entry):
                            database.mark_uploaded(entry)
            else:
                logging.warning("Unable to access server, logging to local database")

    def _upload_entry(self, database_entry:database.DataEntry):
        try:
            requests.get(f"{self.base_url}/upload_data_live/{self.node_key}/{database_entry.sensor_name}/{database_entry.sensor_value}")
            return True
        except:
            return False
