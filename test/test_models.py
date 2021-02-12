import pytest

from restfulcolors.color_utils import ColorValidationError

from restfulcolors.models import (
    Color,
    ColorSchema,
    SimpleColor,
    SimpleColorSchema,
)


def test_simplecolor():
    hexcode = '191900'
    sc = SimpleColor(hexcode)
    assert str(sc) == hexcode

    # test that it won't accept a bad hex code
    hexcode2 = '191900f'
    with pytest.raises(ColorValidationError):
        sc2 = SimpleColor(hexcode2)


def test_color():
    hexcode = 'FFFFFF'
    c = Color(hexcode)

    assert c.attributes['rgb'] == (255,255,255)
    assert c.attributes['hsl'] == (0,0,1.0)
    assert c.attributes['hsv'] == (0,0,1.0)
    assert c.attributes['cmyk'] == (0,0,0,0)
    assert str(c.links['complement'][0]) == '000000'
    assert str(c.links['triad'][0]) == 'ffff00'
    assert str(c.links['triad'][1]) == '00ffff'

