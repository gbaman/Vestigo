from flask import Blueprint, render_template

air_routes = Blueprint('air_routes', __name__, template_folder='templates')

@air_routes.route("/")
def home():
    return render_template("index.html")