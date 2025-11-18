#!/usr/bin/env python

"""Update the OpenAPI schema from the Polar API.

Copyright (c) 2025 Edgar Ramírez-Mondragón
"""

from __future__ import annotations

import http
import json
import logging
import pathlib
import sys
import tempfile
import urllib.request
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from http.client import HTTPResponse

OPENAPI_URL = "https://api.polar.sh/openapi.json"
PATH = "tap_polarsh/openapi/openapi.json"

logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger()


def main() -> None:
    """Update the OpenAPI schema from the Polar API."""
    logger.info("Updating OpenAPI schema from %s", OPENAPI_URL)
    request = urllib.request.Request(OPENAPI_URL, headers={"User-Agent": "tap-polarsh"})  # noqa: S310
    with (
        tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8") as f_out,
        urllib.request.urlopen(request) as f_req,  # noqa: S310
    ):
        f_req = cast("HTTPResponse", f_req)
        if f_req.status != http.HTTPStatus.OK:
            logger.error("Failed to fetch OpenAPI spec: %s", f_req.reason)
            sys.exit()
        spec = json.load(f_req)
        content = json.dumps(spec, indent=2) + "\n"
        f_out.write(content)

    pathlib.Path(f_out.name).rename(PATH)


if __name__ == "__main__":
    main()
