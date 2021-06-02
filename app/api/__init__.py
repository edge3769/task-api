from flask import Blueprint

bp = Blueprint('api', __name__, url_prefix='/1854496672:AAEB8tdvXSsqG57eb5LyOkNbaIIAvXMQmLo')

from app.api import bot
