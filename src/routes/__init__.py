from flask import Blueprint
from flask_restful import Api

from resources.ping import Ping
from resources.report import Report

api_bp = Blueprint("api", __name__)
api = Api(api_bp)

# Ping
api.add_resource(Ping, "/ping")

