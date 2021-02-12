from collections import namedtuple

from marshmallow import Schema, fields

from .color_utils import (
    hex_to_rgb,
    rectangle_tetradic_colors,
    rgb_complement,
    rgb_to_cmyk,
    rgb_to_hex,
    rgb_to_hsl,
    rgb_to_hsv,
    triadic_colors,
)
from .constants import URL_BASE


# Some immutable storage types in a few different color spaces
RgbColor = namedtuple('RgbColor', ['R', 'G', 'B'])
HsvColor = namedtuple('HsvColor', ['H', 'S', 'V'])
HslColor = namedtuple('HslColor', ['H', 'S', 'L'])
CmykColor = namedtuple('CmykColor', ['C', 'M', 'Y', 'K'])


class SimpleColor:
    """A color stored as just a hex colorcode"""
    def __init__(self, colorcode):
        self.colorcode = rgb_to_hex(*hex_to_rgb(colorcode)) 

    def __repr__(self):
        return f'<{self.__class__.__name__}(colorcode="{self.colorcode}")>'

    def __str__(self):
        return self.colorcode


class SimpleColorSchema(Schema):
    """Serializer schema for SimpleColor"""
    href = fields.Function(lambda obj: f'{URL_BASE}/{obj.colorcode}')
    colorcode = fields.String()

    class Meta:
        ordered = True


class Color(SimpleColor):
    """A fuller Color class, with derived information"""
    def __init__(self, colorcode):
        super().__init__(colorcode)
        self.attributes = {}
        self.attributes['rgb'] = RgbColor(*hex_to_rgb(colorcode))
        self.attributes['hsl'] = HslColor(*rgb_to_hsl(*self.attributes['rgb']))
        self.attributes['hsv'] = HsvColor(*rgb_to_hsv(*self.attributes['rgb']))
        self.attributes['cmyk'] = CmykColor(*rgb_to_cmyk(*self.attributes['rgb']))
        self.links = {}
        self.links['complement'] = [ SimpleColor(rgb_to_hex(*rgb_complement(*self.attributes['rgb']))) ]

        triad = triadic_colors(*self.attributes['rgb'])
        self.links['triad'] = [SimpleColor(c) for c in triad]
        tetrad = rectangle_tetradic_colors(*self.attributes['rgb'])
        self.links['tetrad'] = [SimpleColor(c) for c in tetrad]


class ColorSchema(SimpleColorSchema):
    attributes = fields.Dict(keys=fields.Str(), values=fields.List(fields.Number()))
    links = fields.Dict(keys=fields.Str(), values=fields.List(fields.Nested(SimpleColorSchema())))
