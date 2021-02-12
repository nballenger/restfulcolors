from flask import Flask, make_response
from flask_restful import Resource, Api

from .color_utils import ColorValidationError
from .constants import URL_BASE
from .models import (
    Color,
    ColorSchema,
    SimpleColor,
    SimpleColorSchema,
)


app = Flask(__name__)
api = Api(app, default_mediatype='application/json')


class RestfulColor(Resource):
    """Read-only representation of a single color"""
    def get(self, colorhex):
        try:
            color_obj = Color(colorhex)
        except ColorValidationError as e:
            return { "Error": str(e) }

        return make_response(ColorSchema().dumps(color_obj))


api.add_resource(RestfulColor, '/api/v1/colors/<string:colorhex>')
