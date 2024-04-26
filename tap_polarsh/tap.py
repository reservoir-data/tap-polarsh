"""Polar tap class."""

from __future__ import annotations

import typing as t

import requests
from singer_sdk import Stream, Tap
from singer_sdk import typing as th
from singer_sdk._singerlib import resolve_schema_references

from tap_polarsh import streams

if t.TYPE_CHECKING:
    from tap_polarsh.client import PolarStream

OPENAPI_URL = "https://api.polar.sh/openapi.json"
STREAMS: t.Sequence[type[PolarStream]] = [
    streams.Organizations,
    streams.Repositories,
    streams.Issues,
]


class TapPolar(Tap):
    """Singer tap for Polar."""

    name = "tap-polarsh"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "token",
            th.StringType,
            required=True,
            description="API Token for Polar",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="Earliest datetime to get data from",
        ),
    ).to_dict()

    def get_openapi_schema(self) -> dict[t.Any, t.Any]:
        """Retrieve Swagger/OpenAPI schema for this API.

        Returns:
            OpenAPI schema.
        """
        return requests.get(OPENAPI_URL, timeout=5).json()  # type: ignore[no-any-return]

    def discover_streams(self) -> list[Stream]:
        """Return a list of discovered streams.

        Returns:
            A list of Neon Serverless Postgres streams.
        """
        streams: list[PolarStream] = []
        openapi_schema = self.get_openapi_schema()

        for stream_type in STREAMS:
            schema = {
                "$ref": f"#/components/schemas/{stream_type.swagger_ref}",
                "components": openapi_schema["components"],
            }
            resolved_schema = resolve_schema_references(schema)
            streams.append(stream_type(tap=self, schema=resolved_schema))

        return sorted(streams, key=lambda x: x.name)
