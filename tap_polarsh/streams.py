"""Stream type classes for tap-polarsh.

Copyright (c) 2024 Edgar Ramírez-Mondragón
"""

from __future__ import annotations

import typing as t

from tap_polarsh.client import PolarStream

if t.TYPE_CHECKING:
    from singer_sdk.helpers.types import Context


class Organizations(PolarStream):
    """Organizations stream."""

    name = "organizations"
    path = "/api/v1/organizations"
    primary_keys = ("id",)
    replication_key = None

    swagger_ref: str = "Organization"

    def get_url_params(
        self,
        context: Context | None,
        next_page_token: int | None,
    ) -> dict[str, t.Any]:
        """Get URL query parameters.

        Args:
            context: The context of the stream.
            next_page_token: The next page token.

        Returns:
            The URL query parameters.
        """
        params = super().get_url_params(context, next_page_token)
        params["is_member"] = self.config.get("is_member", False)
        return params

    def generate_child_contexts(  # noqa: PLR6301
        self,
        record: dict[str, t.Any],
        context: Context | None,  # noqa: ARG002
    ) -> t.Iterable[dict[str, t.Any] | None]:
        """Generate child contexts.

        Args:
            record: The record.
            context: The context of the stream.

        Yields:
            The child contexts.
        """
        yield {
            "organization_id": record["id"],
        }


class CheckoutLinks(PolarStream):
    """Checkout links stream."""

    name = "checkout_links"
    path = "/api/v1/checkout-links"
    primary_keys = ("id",)

    swagger_ref: str = "CheckoutLink"

    parent_stream_type = Organizations

    def get_url_params(
        self,
        context: Context | None,
        next_page_token: int | None,
    ) -> dict[str, t.Any]:
        """Get URL query parameters.

        Args:
            context: The context of the stream.
            next_page_token: The next page token.

        Returns:
            The URL query parameters.
        """
        return {
            **super().get_url_params(context, next_page_token),
            "organization_id": context["organization_id"] if context else None,
        }


class _BaseBenefits(PolarStream):
    """Base benefits stream."""

    path = "/api/v1/benefits"
    primary_keys = ("id",)

    parent_stream_type = Organizations

    benefit_type: str

    def get_url_params(
        self,
        context: Context | None,
        next_page_token: int | None,
    ) -> dict[str, t.Any]:
        """Get URL query parameters.

        Args:
            context: The context of the stream.
            next_page_token: The next page token.

        Returns:
            The URL query parameters.
        """
        return {
            **super().get_url_params(context, next_page_token),
            "organization_id": context["organization_id"] if context else None,
            "type": self.benefit_type,
        }

    def get_child_context(  # noqa: PLR6301
        self,
        record: dict[str, t.Any],
        context: Context | None,  # noqa: ARG002
    ) -> dict[str, t.Any]:
        """Get child context.

        Args:
            record: The record.
            context: The context of the stream.

        Returns:
            The child context.
        """
        return {
            "benefit_id": record["id"],
        }


class BenefitsCustom(_BaseBenefits):
    """Custom benefits stream."""

    name = "benefits_custom"
    benefit_type = "custom"
    swagger_ref: str = "BenefitCustom"


class BenefitsDiscord(_BaseBenefits):
    """Discord benefits stream."""

    name = "benefits_discord"
    benefit_type = "discord"
    swagger_ref: str = "BenefitDiscord"


class BenefitsGitHubRepo(_BaseBenefits):
    """Benefits stream."""

    name = "benefits_github_repo"
    benefit_type = "github_repository"
    swagger_ref: str = "BenefitGitHubRepository"


class BenefitsDownloadables(_BaseBenefits):
    """Downloadable benefits stream."""

    name = "benefits_downloadables"
    benefit_type = "downloadables"
    swagger_ref: str = "BenefitDownloadables"


class BenefitsLicenseKeys(_BaseBenefits):
    """License keys benefits stream."""

    name = "benefits_license_keys"
    benefit_type = "license_keys"
    swagger_ref: str = "BenefitLicenseKeys"


class BenefitsMeterCredit(_BaseBenefits):
    """Meter credit benefits stream."""

    name = "benefits_meter_credit"
    benefit_type = "meter_credit"
    swagger_ref: str = "BenefitMeterCredit"


class BenefitGrants(PolarStream):
    """Base benefits grants stream."""

    name = "benefit_grants"
    path = "/api/v1/benefits/{benefit_id}/grants"
    primary_keys = ("id",)

    swagger_ref: str = "BenefitGrant"
