"""Tests for the overlay resolver."""

from __future__ import annotations

from pathlib import Path

import pytest

from sop_agent.overlay import OverlayNotFoundError, resolve_overlay
from sop_agent.overlay.loader import ENV_VAR, InvalidOverlayError


def _make_valid_overlay(root: Path) -> Path:
    """Create a minimally-valid overlay at root."""
    (root / "governance").mkdir(parents=True, exist_ok=True)
    (root / "org-map").mkdir(parents=True, exist_ok=True)
    return root


def test_flag_wins_when_provided(tmp_path: Path) -> None:
    overlay = _make_valid_overlay(tmp_path / "explicit")
    config = resolve_overlay(overlay, env={ENV_VAR: "/nonexistent/path"})

    assert config.is_active
    assert config.source == "flag"
    assert config.path == overlay.resolve()


def test_env_used_when_no_flag(tmp_path: Path) -> None:
    overlay = _make_valid_overlay(tmp_path / "from-env")
    config = resolve_overlay(None, env={ENV_VAR: str(overlay)})

    assert config.is_active
    assert config.source == "env"
    assert config.path == overlay.resolve()


def test_fallback_when_nothing_resolves(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # Monkey-patch the auto-discovery path to something that won't exist.
    monkeypatch.setattr(
        "sop_agent.overlay.loader.AUTO_DISCOVERY_PATH",
        tmp_path / "definitely-not-here",
    )
    config = resolve_overlay(None, env={})

    assert not config.is_active
    assert config.source == "fallback"
    assert config.path is None


def test_flag_missing_path_raises(tmp_path: Path) -> None:
    with pytest.raises(OverlayNotFoundError):
        resolve_overlay(tmp_path / "does-not-exist", env={})


def test_env_missing_path_falls_through(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A non-existent env path should silently fall through, not raise.

    This matters for dev environments where the env var is set globally but
    the path may not exist on every machine.
    """
    monkeypatch.setattr(
        "sop_agent.overlay.loader.AUTO_DISCOVERY_PATH",
        tmp_path / "not-here",
    )
    config = resolve_overlay(None, env={ENV_VAR: "/totally/fake/path"})

    assert config.source == "fallback"


def test_overlay_without_subdirs_is_invalid(tmp_path: Path) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()
    with pytest.raises(InvalidOverlayError):
        resolve_overlay(empty, env={})


def test_overlay_with_only_governance_is_valid(tmp_path: Path) -> None:
    overlay = tmp_path / "partial"
    overlay.mkdir()
    (overlay / "governance").mkdir()

    config = resolve_overlay(overlay, env={})
    assert config.is_active
    assert config.governance_dir is not None
    assert config.org_map_dir is None
