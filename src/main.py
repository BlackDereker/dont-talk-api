from dynaconf import FlaskDynaconf
from flask import Flask
from flask.helpers import locked_cached_property
from flask_cors import CORS

from common.formatter_logger import log
from common.util import json_encoding, logutils
from config import FLASK_DEBUG, FLASK_HOST, FLASK_PORT, LOG_NAME
from routes import api_bp

logger = log.getLogger(LOG_NAME)
log.logging.captureWarnings(True)

class LoggerFlask(Flask):
    @locked_cached_property
    def logger(self):
        return log.getLogger()

class MyConfig(object):
    RESTFUL_JSON = {"cls": json_encoding.CustomJSONEncoder}  # add whatever settings here

    @staticmethod
    def init_app(app):
        app.config["RESTFUL_JSON"]["cls"] = app.json_encoder = json_encoding.CustomJSONEncoder
        app.config["PROFILE"] = False


app = Flask(__name__)
app.config.from_object(MyConfig)
MyConfig.init_app(app)
FlaskDynaconf(app)
CORS(app)

# blue print
app.register_blueprint(api_bp, url_prefix="/api")


@app.before_request
def add_log_request_id():
    logger.set(request_id=logutils.request_id())


@app.after_request
def add_request_id_header(response):
    logger.set(request_id=None)
    response.headers["X-Request-ID"] = logutils.request_id()
    return response


if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=int(FLASK_PORT), debug=FLASK_DEBUG)
