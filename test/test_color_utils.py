import pytest

from restfulcolors.color_utils import (
    ColorValidationError,
    hex_to_rgb,
    rgb_to_hex,
    rgb_to_hsl,
    hsl_to_rgb,
    rgb_to_hsv,
    rgb_to_cmyk,
    rgb_complement,
    triadic_colors,
    rectangle_tetradic_colors,
)


class TestColorUtils:
    def test_hex_to_rgb(self):
        assert hex_to_rgb('FFFFFF') == (255,255,255)
        assert hex_to_rgb('000000') == (0, 0, 0)
        assert hex_to_rgb('FF0000') == (255, 0, 0)
        assert hex_to_rgb('c0c0c0') == (192, 192, 192)

        # allow leading hash
        assert hex_to_rgb('#FFFFFF') == (255,255,255)

        # raise exception on bad input
        with pytest.raises(ColorValidationError):
            hex_to_rgb('foo')

    def test_rgb_to_hex(self):
        assert rgb_to_hex(255, 255, 255) == 'ffffff'
        assert rgb_to_hex(192, 192, 192) == 'c0c0c0'

    def test_rgb_to_hsl(self):
        assert rgb_to_hsl(0,0,255) == (240, 1.0, 0.5)
        assert rgb_to_hsl(128,128,0) == (60, 1.0, 0.25)

    def test_rgb_to_hsv(self):
        assert rgb_to_hsv(128,0,0) == (0, 1.0, 0.5)
        assert rgb_to_hsv(128,0,128) == (300, 1.0, 0.5)

    def test_hsl_to_rgb(self):
        assert hsl_to_rgb(240, 1.0, 0.5) == (0,0,255)
        assert hsl_to_rgb(60, 1.0, 0.25) == (127, 127, 0)

    def test_rgb_to_cmyk(self):
        assert rgb_to_cmyk(255,0,0) == (0, 100.0, 100.0, 0)
