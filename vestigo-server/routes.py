import shutil
import tempfile
import weakref

from flask import Blueprint, render_template, send_file
import database
import csv


class FileRemover(object):
    def __init__(self):
        self.weak_references = dict()  # weak_ref -> filepath to remove

    def cleanup_once_done(self, response, filepath):
        wr = weakref.ref(response, self._do_cleanup)
        self.weak_references[wr] = filepath

    def _do_cleanup(self, wr):
        filepath = self.weak_references[wr]
        print('Deleting %s' % filepath)
        shutil.rmtree(filepath, ignore_errors=True)


file_remover = FileRemover()


monitor_routes = Blueprint('monitor_routes', __name__, template_folder='templates')


@monitor_routes.route("/")
def home():
    return render_template("index.html")


@monitor_routes.route("/render/<node_id>/<data_key>/<hours>")
@monitor_routes.route("/render/<node_id>/<data_key>")
def render_chart(node_id, data_key, hours=24):
    data = database.get_data_by_node_id_key(int(node_id), data_key, int(hours))
    template = render_template("render_chart.html", data=data, data_key=data_key, node_id=node_id)
    return template


@monitor_routes.route("/upload_data_live/<node_key>/<data_key>/<data_value>")
def upload_data_live(node_key, data_key, data_value):
    node = database.get_node_from_node_key(node_key)
    if node:
        database.add_data(node, data_key, data_value)
    else:
        return "No node found", 401
    return "True"

@monitor_routes.route("/export/<node_id>/<data_key>/<hours>")
@monitor_routes.route("/export/<node_id>/<data_key>")
def export_csv(node_id, data_key, hours=24):
    with tempfile.NamedTemporaryFile('w', delete=False) as csv_file:
        out_csv = csv.writer(csv_file)
        data = database.get_data_by_node_id_key(int(node_id), data_key, int(hours))
        out_csv.writerow(["Node", "Date", "Time", "Value"])
        for row in data:
            out_csv.writerow([row.data_entry_key, row.data_entry_date_time.strftime('%Y/%m/%d'),  row.data_entry_date_time.strftime('%H:%M:%S'), row.data_entry_value])
        resp = send_file(csv_file.name, as_attachment=True, attachment_filename='data.csv')
        file_remover.cleanup_once_done(resp, csv_file.name)
    return resp