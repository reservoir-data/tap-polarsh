"""Polar tap class.

Copyright (c) 2024 Edgar Ramírez-Mondragón
"""

from __future__ import annotations

from typing import override

from singer_sdk import Stream, Tap
from singer_sdk import typing as th

from tap_polarsh import streams


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

    @override
    def discover_streams(self) -> list[Stream]:
        """Return a list of discovered streams.

        Returns:
            A list of Neon Serverless Postgres streams.
        """
        return [
            streams.Organizations(tap=self),
            streams.CheckoutLinks(tap=self),
            streams.Products(tap=self),
            streams.Subscriptions(tap=self),
            streams.Orders(tap=self),
            streams.BenefitsCustom(tap=self),
            streams.BenefitGrantsCustom(tap=self),
            streams.BenefitsDiscord(tap=self),
            streams.BenefitGrantsDiscord(tap=self),
            streams.BenefitsGitHubRepo(tap=self),
            streams.BenefitGrantsGitHubRepo(tap=self),
            streams.BenefitsDownloadables(tap=self),
            streams.BenefitGrantsDownloadables(tap=self),
            streams.BenefitsLicenseKeys(tap=self),
            streams.BenefitGrantsLicenseKeys(tap=self),
            streams.BenefitsMeterCredit(tap=self),
            streams.BenefitGrantsMeterCredit(tap=self),
        ]
