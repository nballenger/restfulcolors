import re


# Regex to extract RGB hex pairs from a six character hex color code
HEXCOLOR_RE = re.compile(r"""^\#?                 # optional leading octothorpe
                             (?P<r>[0-9a-f]{2})   # hex pair for red
                             (?P<g>[0-9a-f]{2})   # hex pair for green
                             (?P<b>[0-9a-f]{2})   # hex pair for blue
                             $""", re.VERBOSE | re.IGNORECASE)


class ColorValidationError(Exception):
     ...


def hex_to_rgb(hex_string):
    """Convert a six digit hex string to three RGB integers, 0-255"""
    m = HEXCOLOR_RE.match(hex_string)
    if not m:
        msg = f"Not a valid hexadecimal color code: '{hex_string}'"
        raise ColorValidationError(msg)

    return tuple([int(m.groupdict()[x], 16) for x in ('r', 'g', 'b')])

def rgb_to_hex(r, g, b):
    """Convert RGB integers, 0-255, to a string of six hex digits"""
    return ''.join([hex(c).split('x')[1].zfill(2) for c in (r, g, b)])

def rgb_to_hsl(r, g, b):
    """
    Convert RGB integers, 0-255, to Hue, Saturation, Lightness values.

    Returns a tuple of (Hue, Saturation, Lightness), where Hue is a
    degree between 0 and 360, and Saturation and Lightness are 0..1
    """
    rgb = [x / 255.0 for x in (r, g, b)]    # normalize to 0..1
    cmin, cmax = min(rgb), max(rgb)
    cdelta = cmax - cmin

    (H, S, L) = (0, 0, 0)

    # Hue calculation
    if cdelta == 0:
        H = 0
    elif cmax == rgb[0]:
        H = 60 * (((rgb[1] - rgb[2]) / cdelta) % 6)
    elif cmax == rgb[1]:
        H = 60 * (((rgb[2] - rgb[0]) / cdelta) + 2)
    elif cmax == rgb[2]:
        H = 60 * (((rgb[0] - rgb[1]) / cdelta) + 4)

    # Lightness calculation
    L = (cmax + cmin) / 2.0

    # Saturation calculation
    if cdelta == 0:
        S = 0
    else:
        S = cdelta / (1 - abs(2 * L - 1))

    return (round(H, 2), round(S, 2), round(L, 2))

def hsl_to_rgb(H, S, L): 
    """Convert Hue, Saturation, and Lightness to Red, Green, Blue"""
    C = (1 - abs(2 * L - 1)) * S 
    X = C * 1 - abs(((H / 60) % 2) - 1)
    m = L - C / 2.0 
    
    if   H >=   0 and H <  60: 
        (R, G, B) = (C, X, 0)
    elif H >=  60 and H < 120:
        (R, G, B) = (X, C, 0)
    elif H >= 120 and H < 180:
        (R, G, B) = (0, C, X)
    elif H >= 180 and H < 240:
        (R, G, B) = (0, X, C)
    elif H >= 240 and H < 300:
        (R, G, B) = (X, 0, C)
    elif H >= 300 and H < 360:
        (R, G, B) = (C, 0, X)

    (r, g, b) = ( (R+m)*255, (G+m)*255, (B+m)*255 )

    return (int(r), int(g), int(b))

def rgb_to_hsv(r, g, b):
    """Convert RGB integers, 0-255, to Hue, Saturation, Value values"""
    rgb = [x / 255.0 for x in (r, g, b)]    # normalize to 0..1
    cmin, cmax = min(rgb), max(rgb)
    cdelta = cmax - cmin

    (H, S, V) = (0, 0, 0)

    # Hue calculation (same as HSL)
    if cdelta == 0:
        H = 0
    elif cmax == rgb[0]:
        H = 60 * (((rgb[1] - rgb[2]) / cdelta) % 6)
    elif cmax == rgb[1]:
        H = 60 * (((rgb[2] - rgb[0]) / cdelta) + 2)
    elif cmax == rgb[2]:
        H = 60 * (((rgb[0] - rgb[1]) / cdelta) + 4)

    # Saturation calculation (NOT the same as HSL)
    if cmax == 0:
        S = 0
    else:
        S = cdelta / cmax

    # Value calculation (also not the same as HSL)
    V = cmax

    return (round(H, 2), round(S, 2), round(V, 2))

def rgb_to_cmyk(r, g, b): 
    """ 
    Convert RGB integers, 0-255, to Cyan, Magenta, Yellow, Black values.

    Returns a tuple of (C, M, Y, K), each a percentage with 2 precision digits.
    """
    rgb = [x / 255.0 for x in (r, g, b)]    # normalize to 0..1
    cmin, cmax = min(rgb), max(rgb)
    cdelta = cmax - cmin

    K = 1 - cmax
    (C, M, Y) = (0, 0, 0)
    
    if K < 1:
        C = (1 - rgb[0] - K) / (1 - K)
        M = (1 - rgb[1] - K) / (1 - K)
        Y = (1 - rgb[2] - K) / (1 - K)

    return (round(C * 100, 2), 
            round(M * 100, 2), 
            round(Y * 100, 2), 
            round(K * 100, 2))

def rgb_complement(r, g, b):
    """Return the complementary color (opposite on color wheel)"""
    return [255 - x for x in [r, g, b]]

def triadic_colors(r, g, b):
    """
    Return two colors that complete an equidistant triad on the color wheel.

    Much easier to do in HSL or HSV space, since it's just a modulo operation
    on the Hue number.
    """
    (H,S,L) = rgb_to_hsl(r, g, b)
    c1 = hsl_to_rgb( (H + 120) % 360, S, L)
    c2 = hsl_to_rgb( (H + 240) % 360, S, L)
    return (rgb_to_hex(*c1), rgb_to_hex(*c2))

def rectangle_tetradic_colors(r, g, b):
    """Return three colors that are 60, 180, and 240 degrees from base color"""
    (H,S,L) = rgb_to_hsl(r, g, b)
    c1 = hsl_to_rgb( (H +  60) % 360, S, L)
    c2 = hsl_to_rgb( (H + 180) % 360, S, L)
    c3 = hsl_to_rgb( (H + 240) % 360, S, L)
    return (rgb_to_hex(*c1), rgb_to_hex(*c2), rgb_to_hex(*c3))

def closest_named_html_color(r, g, b):
    """
    I'm not implementing this because I don't want to spend the time
    to do it efficiently, but it'd be fun to calculate the lowest
    Euclidean / Minkowski distance to one of the HTML named colors.
    """
    return "Not today, I'm afraid."
