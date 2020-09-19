import tempfile

from flask import Blueprint, render_template, send_file
import database
import csv

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
    return "True"

@monitor_routes.route("/export/<node_id>/<data_key>/<hours>")
@monitor_routes.route("/export/<node_id>/<data_key>")
def export_csv(node_id, data_key, hours=24):
    with tempfile.NamedTemporaryFile('w') as csv_file:
        out_csv = csv.writer(csv_file)
        data = database.get_data_by_node_id_key(int(node_id), data_key, int(hours))
        out_csv.writerow(["Node", "Value", "Date"])
        for row in data:
            out_csv.writerow([row.data_entry_key, row.data_entry_value, row.data_entry_date_time])
        return send_file(csv_file.name, as_attachment=True, attachment_filename='data.csv')