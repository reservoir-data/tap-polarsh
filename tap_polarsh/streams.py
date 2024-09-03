"""Stream type classes for tap-polarsh."""

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

    swagger_ref: str = "Organization-Output"

    def get_url_params(
        self,
        context: Context | None,
        next_page_token: int | None,
    ) -> dict[str, t.Any]:
        """Get URL query parameters."""
        params = super().get_url_params(context, next_page_token)
        params["is_member"] = self.config.get("is_member", False)
        return params

    def generate_child_contexts(
        self,
        record: dict[str, t.Any],
        context: Context | None,  # noqa: ARG002
    ) -> t.Iterable[dict[str, t.Any] | None]:
        """Generate child contexts."""
        yield {
            "organization_id": record["id"],
        }


class Repositories(PolarStream):
    """Repositories stream."""

    name = "repositories"
    path = "/api/v1/repositories"
    primary_keys = ("id",)
    replication_key = None

    swagger_ref: str = "Repository-Output"

    parent_stream_type = Organizations

    def get_url_params(
        self,
        context: Context | None,
        next_page_token: int | None,
    ) -> dict[str, t.Any]:
        """Get URL query parameters."""
        return {
            **super().get_url_params(context, next_page_token),
            "organization_id": context["organization_id"] if context else None,
        }


class OrganizationCustomers(PolarStream):
    """Organization customers stream.

    DEPRECATED: This stream is no longer supported.
    """

    name = "organization_customers"
    path = "/api/v1/organizations/{organization_id}/customers"
    primary_keys = (
        "organization_id",
        "public_name",
    )
    replication_key = None

    swagger_ref: str = "OrganizationCustomer"

    parent_stream_type = Organizations

    @property
    def schema(self) -> dict[str, t.Any]:
        """Generate schema."""
        schema = super().schema
        schema["properties"]["organization_id"] = {"type": ["string", "null"]}
        return schema


class Articles(PolarStream):
    """Issues stream."""

    name = "articles"
    path = "/api/v1/articles"
    primary_keys = ("id",)
    replication_key = None

    swagger_ref: str = "Article"

    parent_stream_type = Organizations

    def get_url_params(
        self,
        context: Context | None,
        next_page_token: t.Any | None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        """Get URL query parameters."""
        return {
            **super().get_url_params(context, next_page_token),
            "organization_id": context["organization_id"] if context else None,
        }
