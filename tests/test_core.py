"""Tests standard tap features using the built-in SDK tests library.

Copyright (c) 2024 Edgar Ramírez-Mondragón
"""

from __future__ import annotations

from typing import Any

from singer_sdk.testing import SuiteConfig, get_tap_test_class

from tap_polarsh.tap import TapPolar

SAMPLE_CONFIG: dict[str, Any] = {}

TestTapPolar = get_tap_test_class(
    TapPolar,
    config=SAMPLE_CONFIG,
    suite_config=SuiteConfig(
        max_records_limit=10,
        ignore_no_records_for_streams=[
            "checkout_links",
        ],
    ),
)
