"""Stream type classes for tap-polarsh.

Copyright (c) 2024 Edgar Ramírez-Mondragón
"""

from __future__ import annotations

from importlib import resources
from typing import TYPE_CHECKING, Any, override

from singer_sdk import OpenAPISchema, StreamSchema

from tap_polarsh import openapi
from tap_polarsh.client import PolarStream

if TYPE_CHECKING:
    from collections.abc import Iterable

    from singer_sdk.helpers.types import Context
    from singer_sdk.streams.rest import HTTPRequest, PageContext

OPENAPI_SCHEMA = OpenAPISchema(resources.files(openapi) / "openapi.json")


class Organizations(PolarStream):
    """Organizations stream."""

    name = "organizations"
    path = "/api/v1/organizations"

    schema = StreamSchema(OPENAPI_SCHEMA, key="Organization")

    @override
    def get_http_request(self, *, context: PageContext) -> HTTPRequest:
        req = super().get_http_request(context=context)
        req.params["is_member"] = self.config.get("is_member", False)
        return req

    @override
    def generate_child_contexts(
        self,
        record: dict[str, Any],
        context: Context | None,
    ) -> Iterable[dict[str, Any] | None]:
        yield {
            "organization_id": record["id"],
        }


class _OrganizationStream(PolarStream):
    """Base class for organization streams."""

    parent_stream_type = Organizations

    @override
    def get_http_request(self, *, context: PageContext) -> HTTPRequest:
        assert context.stream_context is not None  # noqa: S101

        req = super().get_http_request(context=context)
        req.params["organization_id"] = context.stream_context["organization_id"]
        return req


class CheckoutLinks(_OrganizationStream):
    """Checkout links stream."""

    name = "checkout_links"
    path = "/api/v1/checkout-links"

    schema = StreamSchema(OPENAPI_SCHEMA, key="CheckoutLink")


class Products(_OrganizationStream):
    """Products stream."""

    name = "products"
    path = "/api/v1/products"

    schema = StreamSchema(OPENAPI_SCHEMA, key="Product")


class Subscriptions(_OrganizationStream):
    """Subscriptions stream."""

    name = "subscriptions"
    path = "/api/v1/subscriptions"

    schema = StreamSchema(OPENAPI_SCHEMA, key="Subscription")


class Orders(_OrganizationStream):
    """Orders stream."""

    name = "orders"
    path = "/api/v1/orders"

    schema = StreamSchema(OPENAPI_SCHEMA, key="Order")


class _BaseBenefits(PolarStream):
    """Base benefits stream."""

    path = "/api/v1/benefits"
    primary_keys = ("id",)

    parent_stream_type = Organizations

    benefit_type: str

    @override
    def get_http_request(self, *, context: PageContext) -> HTTPRequest:
        request = super().get_http_request(context=context)
        request.params["organization_id"] = (
            context.stream_context["organization_id"]
            if context.stream_context
            else None,
        )
        request.params["type"] = self.benefit_type
        return request

    @override
    def get_child_context(
        self,
        record: dict[str, Any],
        context: Context | None,
    ) -> dict[str, Any]:
        return {
            "benefit_id": record["id"],
        }


class BenefitsCustom(_BaseBenefits):
    """Custom benefits stream."""

    name = "benefits_custom"
    benefit_type = "custom"

    schema = StreamSchema(OPENAPI_SCHEMA, key="BenefitCustom")


class BenefitsDiscord(_BaseBenefits):
    """Discord benefits stream."""

    name = "benefits_discord"
    benefit_type = "discord"

    schema = StreamSchema(OPENAPI_SCHEMA, key="BenefitDiscord")


class BenefitsGitHubRepo(_BaseBenefits):
    """Benefits stream."""

    name = "benefits_github_repo"
    benefit_type = "github_repository"

    schema = StreamSchema(OPENAPI_SCHEMA, key="BenefitGitHubRepository")


class BenefitsDownloadables(_BaseBenefits):
    """Downloadable benefits stream."""

    name = "benefits_downloadables"
    benefit_type = "downloadables"

    schema = StreamSchema(OPENAPI_SCHEMA, key="BenefitDownloadables")


class BenefitsLicenseKeys(_BaseBenefits):
    """License keys benefits stream."""

    name = "benefits_license_keys"
    benefit_type = "license_keys"

    schema = StreamSchema(OPENAPI_SCHEMA, key="BenefitLicenseKeys")


class BenefitsMeterCredit(_BaseBenefits):
    """Meter credit benefits stream."""

    name = "benefits_meter_credit"
    benefit_type = "meter_credit"

    schema = StreamSchema(OPENAPI_SCHEMA, key="BenefitMeterCredit")


class BenefitGrants(PolarStream):
    """Base benefits grants stream."""

    name = "benefit_grants"
    path = "/api/v1/benefits/{benefit_id}/grants"
    primary_keys = ("id",)

    schema = StreamSchema(OPENAPI_SCHEMA, key="BenefitGrant")

    parent_stream_type = BenefitsGitHubRepo
