from flask import Blueprint, render_template
import database

monitor_routes = Blueprint('monitor_routes', __name__, template_folder='templates')


@monitor_routes.route("/")
def home():
    return render_template("index.html")


@monitor_routes.route("/render/<node_id>/<data_key>/<hours>")
@monitor_routes.route("/render/<node_id>/<data_key>")
def render_chart(node_id, data_key, hours=24):
    data = database.get_data_by_node_id_key(int(node_id), data_key, int(hours))
    template = render_template("render_chart.html", data=data, data_key=data_key)
    return template


@monitor_routes.route("/upload_data_live/<node_key>/<data_key>/<data_value>")
def upload_data_live(node_key, data_key, data_value):
    node = database.get_node_from_node_key(node_key)
    if node:
        database.add_data(node, data_key, data_value)
    return "True"