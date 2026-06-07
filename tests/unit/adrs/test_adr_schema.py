import re
import pytest

from pathlib import Path


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").is_file():
            return parent
    raise RuntimeError("could not locate repo root (no pyproject.toml found)")


ADR_DIR = _repo_root() / "adrs"

REQUIRED_HEADINGS = (
    "Date",
    "Status",
    "Context",
    "Decision",
    "Alternatives considered",
    "Consequences",
    "Re-baseline impact",
    "Reversal trigger",
)

TITLE_RE = re.compile(r"^# ADR-\d{4}:\s+\S", re.MULTILINE)
H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


def _adr_files() -> list[Path]:
    return sorted(ADR_DIR.glob("ADR-*.md"))


def test_adr_files_are_discovered() -> None:
    assert _adr_files(), f"no ADR-*.md files found under {ADR_DIR}"


@pytest.mark.parametrize("adr", _adr_files(), ids=lambda p: p.name)
def test_adr_has_title(adr: Path) -> None:
    text = adr.read_text()
    assert TITLE_RE.search(text), f"{adr.name} is missing a '# ADR-NNNN: <description>' title heading"


@pytest.mark.parametrize("adr", _adr_files(), ids=lambda p: p.name)
def test_adr_has_required_headings(adr: Path) -> None:
    text = adr.read_text(encoding="utf-8")
    headings = {m.group(1).strip() for m in H2_RE.finditer(text)}
    missing = [h for h in REQUIRED_HEADINGS if h not in headings]
    assert not missing, f"{adr.name} is missing required heading(s): {missing}"
