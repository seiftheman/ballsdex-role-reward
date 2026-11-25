"""Sphinx configuration for the ballsdex-role-reward documentation."""

from __future__ import annotations

import tomllib
from pathlib import Path

project = "ballsdex-role-reward"
author = "Seif"
copyright = "2026, Seif"

_pyproject = tomllib.loads((Path(__file__).resolve().parent.parent / "pyproject.toml").read_text(encoding="utf-8"))
release = _pyproject["project"]["version"]
version = release

extensions = [
    "myst_parser",
]

source_suffix = {
    ".md": "markdown",
}
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

myst_enable_extensions = [
    "colon_fence",
    "deflist",
]
myst_heading_anchors = 3

html_theme = "furo"
html_title = f"{project} {release}"
html_theme_options = {
    "sidebar_hide_name": False,
}
