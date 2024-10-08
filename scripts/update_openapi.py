#!/usr/bin/env python
# /// script
# dependencies = [
#   "requests>=2.25.1",
# ]
# ///

"""Update the OpenAPI schema from the Polar API."""

from __future__ import annotations

import pathlib

import requests

OPENAPI_URL = "https://api.polar.sh/openapi.json"
PATH = "tap_polarsh/openapi/openapi.json"


with pathlib.Path(PATH).open("w") as file:
    file.write(requests.get(OPENAPI_URL, timeout=5).text)
