from dynaconf import settings

from common.formatter_logger import log
from common.formatter_logger.utils import config_validator

LOG_NAME = settings.get("LOG_NAME", "dont-talk-api", fresh=True)
logger = log.getLogger(LOG_NAME)

variables = [
    {"name": "ENV_FOR_DYNACONF", "default": "default", "dynaconf": True},
    {"name": "FLASK_DEBUG", "default": settings.get("FLASK_DEBUG", fresh=True), "dynaconf": True},
    {"name": "FLASK_PORT", "default": settings.get("FLASK_PORT", 8000, fresh=True), "dynaconf": True},
    {"name": "FLASK_HOST", "default": settings.get("FLASK_HOST", fresh=True), "dynaconf": True},
]

try:
    (  # pylint: disable=E0632
        ENV_FOR_DYNACONF,
        FLASK_DEBUG,
        FLASK_PORT,
        FLASK_HOST,
    ) = config_validator(variables)
except Exception:
    logger.exception("Can't continue due to error in configuration")
    exit(1)

print("Configuration completed!")