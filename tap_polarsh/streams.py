"""Stream type classes for tap-polarsh."""

from __future__ import annotations

import typing as t

from tap_polarsh.client import PolarStream


class Organizations(PolarStream):
    """Organizations stream."""

    name = "organizations"
    path = "/api/v1/organizations"
    primary_keys = ("id",)
    replication_key = None

    swagger_ref: str = "Organization"

    def generate_child_contexts(
        self,
        record: dict[str, t.Any],
        context: dict[str, t.Any] | None,  # noqa: ARG002
    ) -> t.Iterable[dict[str, t.Any] | None]:
        """Generate child contexts."""
        yield {
            "organization_id": record["id"],
            "organization_name": record["name"],
            "platform": record["platform"],
        }


class Repositories(PolarStream):
    """Repositories stream."""

    name = "repositories"
    path = "/api/v1/repositories"
    primary_keys = ("id",)
    replication_key = None

    swagger_ref: str = "Repository-Output"


class Issues(PolarStream):
    """Issues stream."""

    name = "issues"
    path = "/api/v1/issues/search"
    primary_keys = ("id",)
    replication_key = None

    swagger_ref: str = "Issue-Output"

    parent_stream_type = Organizations

    def get_url_params(
        self,
        context: dict[str, t.Any] | None,
        next_page_token: t.Any | None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        """Get URL query parameters."""
        return {
            **super().get_url_params(context, next_page_token),
            "platform": context["platform"] if context else None,
            "organization_name": context["organization_name"] if context else None,
        }
