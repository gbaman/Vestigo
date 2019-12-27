from flask import Blueprint, render_template
import database

air_routes = Blueprint('air_routes', __name__, template_folder='templates')

@air_routes.route("/")
def home():
    return render_template("index.html")


@air_routes.route("/upload_data_live/<node_key>/<data_key>/<data_value>")
def upload_data_live(node_key, data_key, data_value):
    node = database.get_node_from_node_key(node_key)
    if node:
        database.add_data(node, data_key, data_value)
    return "True"