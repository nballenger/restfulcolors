# RESTful Colors API

This is a Flask application with a single endpoint at `/api/v1/colors/{some-hex-color-code}`. It returns a JSON response about the color supplied in the URL.

## Installation

The app was created via [pipenv](https://pypi.org/project/pipenv/), and can be installed with its dependencies by running:

```Shell
git clone https://github.com/nballenger/restfulcolors.git
cd restfulcolors
pipenv install
```

Alternatively, the dependencies may be installed manually via pip:

```Shell
pip install flask flask-restful marshmallow pytest
```

## Running the App

The app currently runs using the Flask development server. To run it on your local host, you can use one of the following commands in the top level of the repo:

```Shell
FLASK_APP=restfulcolors pipenv run flask run
```

or, if you aren't using pipenv

```Shell
FLASK_APP=restfulcolors flask run
```

### Example Request / Response

The endpoint only responds to GET requests, and must end in a valid, six digit hexadecimal color code.

For instance, a request with the color code for <span style="background-color: #191970;color: #FFFFFF;">Midnight Blue</span> would be made to:

```
http://127.0.0.1:5000/api/v1/colors/191970
```

and would receive a response like the following:

```JSON
{
  "href": "/api/v1/colors/191970",
  "colorcode": "191970",
  "attributes": {
    "rgb": [ 25, 25, 112 ],
    "hsl": [ 240, 0.64, 0.27 ],
    "hsv": [ 240, 0.78, 0.44 ],
    "cmyk": [ 77.68, 77.68, 0, 56.08 ]
  },
  "links": {
    "complement": [
      {
        "href": "/api/v1/colors/e6e68f",
        "colorcode": "e6e68f"
      }
    ],
    "triad": [
      {
        "href": "/api/v1/colors/708e18",
        "colorcode": "708e18"
      },
      {
        "href": "/api/v1/colors/18708e",
        "colorcode": "18708e"
      }
    ],
    "tetrad": [
      {
        "href": "/api/v1/colors/701870",
        "colorcode": "701870"
      },
      {
        "href": "/api/v1/colors/707018",
        "colorcode": "707018"
      },
      {
        "href": "/api/v1/colors/18708e",
        "colorcode": "18708e"
      }
    ]
  }
}
```

## Testing

Running `pytest` should execute all the current tests. 
