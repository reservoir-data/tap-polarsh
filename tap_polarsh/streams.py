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
