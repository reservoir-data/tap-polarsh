#!/usr/bin/env python
# /// script
# dependencies = [
#   "requests>=2.25.1",
# ]
# ///

"""Update the OpenAPI schema from the Polar API."""

from __future__ import annotations

import json
import pathlib

import requests

OPENAPI_URL = "https://api.polar.sh/openapi.json"
PATH = "tap_polarsh/openapi/openapi.json"


def main() -> None:
    """Update the OpenAPI schema from the Polar API."""
    with pathlib.Path(PATH).open("w") as file:
        response = requests.get(OPENAPI_URL, timeout=5)
        response.raise_for_status()
        spec = response.json()

        content = json.dumps(spec, indent=2) + "\n"
        file.write(content)


if __name__ == "__main__":
    main()
