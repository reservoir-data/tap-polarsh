"""REST client handling, including PolarStream base class.

Copyright (c) 2024 Edgar Ramírez-Mondragón
"""

from __future__ import annotations

import sys
import typing as t

from singer_sdk import RESTStream
from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.pagination import BasePageNumberPaginator

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if t.TYPE_CHECKING:
    from singer_sdk.helpers.types import Context


class PolarStream(RESTStream[t.Any]):
    """Polar stream class."""

    url_base = "https://api.polar.sh"
    records_jsonpath = "$.items[*]"
    primary_keys = ("id",)

    page_size = 100
    """Number of records to request per API call."""

    @property
    @override
    def authenticator(self) -> BearerTokenAuthenticator:
        """Get an authenticator object.

        Returns:
            The authenticator instance for this REST stream.
        """
        return BearerTokenAuthenticator(token=self.config["token"])

    def get_new_paginator(self) -> BasePageNumberPaginator:  # noqa: PLR6301
        """Get a new paginator object.

        Returns:
            A new paginator object.
        """
        return BasePageNumberPaginator(start_value=1)

    @override
    def get_url_params(
        self,
        context: Context | None,
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
