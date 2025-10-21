"""Test schema evolution.

Copyright (c) 2024 Edgar Ramírez-Mondragón
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from syrupy.extensions.json import JSONSnapshotExtension

if TYPE_CHECKING:
    import pytest
    from pytest_subtests.plugin import SubTests
    from syrupy.assertion import SnapshotAssertion


def test_catalog_changes(
    pytester: pytest.Pytester,
    snapshot: SnapshotAssertion,
    subtests: SubTests,
) -> None:
    """Fail if the catalog has changed."""
    result = pytester.run("tap-polarsh", "--discover")
    assert result.ret == 0, "Tap discovery failed"

    snapshot_json = snapshot.with_defaults(extension_class=JSONSnapshotExtension)

    catalog = json.loads("".join(result.outlines))
    for stream in catalog["streams"]:
        stream_id = stream["tap_stream_id"]
        with subtests.test(stream_id):
            assert snapshot_json(name=stream_id) == stream
