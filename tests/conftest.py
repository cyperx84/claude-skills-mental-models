"""Shared fixtures.

Every test that changes the content root restores auto-detection afterwards, and
no test writes to a real home or config directory.
"""

from __future__ import annotations

import pytest

from mental_models_kit import set_content_root

_FIXTURE = """## Mental Model = {name}

**Category = {detail}**
**Description:**
{desc}

**When to Avoid (or Use with Caution):**
- Never on Tuesdays.

**Keywords for Situations:**
{kw}.

**Thinking Steps:**
1. Think.

**Coaching Questions:**
- "Really?"
"""


@pytest.fixture(autouse=True)
def _restore_content_root():
    """Guarantee no test leaks a content-root override into the next one."""
    yield
    set_content_root(None)


@pytest.fixture
def fixture_root(tmp_path):
    """A throwaway content root holding two synthetic models."""
    general = tmp_path / "Mental_Model_General"
    war = tmp_path / "Mental_Model_War"
    general.mkdir()
    war.mkdir()
    (general / "m01_alpha_thing.md").write_text(
        _FIXTURE.format(
            name="Alpha Thing",
            detail="General Thinking Tools",
            desc="A synthetic model used only by the test suite.",
            kw="alpha, testing, synthetic",
        ),
        encoding="utf-8",
    )
    (war / "m02_beta's_thing.md").write_text(
        _FIXTURE.format(
            name="Beta's Thing",
            detail="Warfare & Nonsense",
            desc="Another synthetic model.",
            kw="beta, testing",
        ),
        encoding="utf-8",
    )
    (tmp_path / "_TEMPLATE.md").write_text("## Mental Model = <Name>\n", encoding="utf-8")
    set_content_root(tmp_path)
    return tmp_path
