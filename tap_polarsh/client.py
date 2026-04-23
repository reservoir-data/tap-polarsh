"""REST client handling, including PolarStream base class.

Copyright (c) 2024 Edgar Ramírez-Mondragón
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from singer_sdk import RESTStream
from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.pagination import PageNumberPaginator

if TYPE_CHECKING:
    from singer_sdk.streams.rest import HTTPRequest, PageContext


class PolarStream(RESTStream[Any]):
    """Polar stream class."""

    url_base = "https://api.polar.sh"
    records_jsonpath = "$.items[*]"
    primary_keys = ("id",)

    page_size = 100
    """Number of records to request per API call."""

    @property
    @override
    def authenticator(self) -> BearerTokenAuthenticator:
        return BearerTokenAuthenticator(token=self.config["token"])

    @override
    def get_new_paginator(self) -> PageNumberPaginator:
        return PageNumberPaginator(start_value=1)

    @override
    def get_http_request(self, *, context: PageContext) -> HTTPRequest:
        req = super().get_http_request(context=context)
        req.params["page"] = context.next_page_token
        req.params["limit"] = self.page_size
        return req
