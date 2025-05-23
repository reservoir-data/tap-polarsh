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


class _OrganizationStream(PolarStream):
    """Base class for organization streams."""

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


class CheckoutLinks(_OrganizationStream):
    """Checkout links stream."""

    name = "checkout_links"
    path = "/api/v1/checkout-links"
    primary_keys = ("id",)

    swagger_ref: str = "CheckoutLink"

    parent_stream_type = Organizations


class Products(_OrganizationStream):
    """Products stream."""

    name = "products"
    path = "/api/v1/products"
    primary_keys = ("id",)

    swagger_ref: str = "Product"

    parent_stream_type = Organizations


class Subscriptions(_OrganizationStream):
    """Subscriptions stream."""

    name = "subscriptions"
    path = "/api/v1/subscriptions"
    primary_keys = ("id",)

    swagger_ref: str = "Subscription"

    parent_stream_type = Organizations


class Orders(_OrganizationStream):
    """Orders stream."""

    name = "orders"
    path = "/api/v1/orders"
    primary_keys = ("id",)

    swagger_ref: str = "Order"

    parent_stream_type = Organizations
