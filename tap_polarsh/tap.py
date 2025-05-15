"""Polar tap class.

Copyright (c) 2024 Edgar Ramírez-Mondragón
"""

from __future__ import annotations

import json
import typing as t
from importlib import resources

from singer_sdk import Stream, Tap
from singer_sdk import typing as th
from singer_sdk.singerlib import resolve_schema_references

from tap_polarsh import openapi, streams

if t.TYPE_CHECKING:
    from tap_polarsh.client import PolarStream

STREAMS: t.Sequence[type[PolarStream]] = [
    streams.Organizations,
    streams.CheckoutLinks,
    streams.Products,
    streams.Subscriptions,
    streams.Orders,
    streams.BenefitsCustom,
    streams.BenefitsDiscord,
    streams.BenefitsGitHubRepo,
    streams.BenefitsDownloadables,
    streams.BenefitsLicenseKeys,
    streams.BenefitsMeterCredit,
    streams.BenefitGrants,
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
            "is_member",
            th.BooleanType,
            description=(
                "Whether to only query organizations the user is a member of. "
                "Defaults to True."
            ),
            default=True,
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="Earliest datetime to get data from",
        ),
    ).to_dict()

    def get_openapi_schema(self) -> dict[t.Any, t.Any]:  # noqa: PLR6301
        """Retrieve Swagger/OpenAPI schema for this API.

        Returns:
            OpenAPI schema.
        """
        with resources.files(openapi).joinpath("openapi.json").open() as file:
            return json.load(file)  # type: ignore[no-any-return]

    def discover_streams(self) -> list[Stream]:
        """Return a list of discovered streams.

        Returns:
            A list of Neon Serverless Postgres streams.
        """
        streams_dict: dict[str, PolarStream] = {}
        openapi_schema = self.get_openapi_schema()

        for stream_type in STREAMS:
            schema = {
                "$ref": f"#/components/schemas/{stream_type.swagger_ref}",
                "components": openapi_schema["components"],
            }
            resolved_schema = resolve_schema_references(schema)
            streams_dict[stream_type.name] = stream_type(
                tap=self,
                schema=resolved_schema,
            )

        for stream_name, stream_type in streams_dict.items():
            if stream_name.startswith("benefits_"):
                stream_type.child_streams.append(streams_dict["benefit_grants"])

        return sorted(streams_dict.values(), key=lambda x: x.name)
