"""REST client handling, including PolarStream base class.

Copyright (c) 2024 Edgar Ramírez-Mondragón
"""

from __future__ import annotations

import typing as t

from singer_sdk import RESTStream
from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.pagination import BasePageNumberPaginator

if t.TYPE_CHECKING:
    from singer_sdk.helpers.types import Context


class PolarStream(RESTStream[t.Any]):
    """Polar stream class."""

    url_base = "https://api.polar.sh"
    records_jsonpath = "$.items[*]"

    swagger_ref: str
    """OpenAPI schema reference for this stream."""

    page_size = 100
    """Number of records to request per API call."""

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        """Get an authenticator object.

        Returns:
            The authenticator instance for this REST stream.
        """
        token: str = self.config["token"]
        return BearerTokenAuthenticator.create_for_stream(
            self,
            token=token,
        )

    @property
    def http_headers(self) -> dict[str, str]:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        return {"User-Agent": f"{self.tap_name}/{self._tap.plugin_version}"}

    def get_new_paginator(self) -> BasePageNumberPaginator:  # noqa: PLR6301
        """Get a new paginator object.

        Returns:
            A new paginator object.
        """
        return BasePageNumberPaginator(start_value=1)

    def get_url_params(
        self,
        context: Context | None,  # noqa: ARG002
        next_page_token: int | None,
    ) -> dict[str, t.Any]:
        """Get URL query parameters.

        Args:
            context: Stream sync context.
            next_page_token: Next offset.

        Returns:
            Mapping of URL query parameters.
        """
        return {
            "page": next_page_token,
            "limit": self.page_size,
        }
