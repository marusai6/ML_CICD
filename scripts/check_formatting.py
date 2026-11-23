"""Lightweight formatting gate; Ruff performs the separate static-analysis stage."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
DIRECTORIES = [ROOT / "app", ROOT / "scripts", ROOT / "tests"]
MAX_LINE_LENGTH = 140
errors = []
for directory in DIRECTORIES:
    for path in sorted(directory.rglob("*.py")):
        if path.name == Path(__file__).name:
            continue
        text = path.read_text(encoding="utf-8")
        if text and not text.endswith("\n"):
            errors.append(f"{path.relative_to(ROOT)}: missing final newline")
        for number, line in enumerate(text.splitlines(), start=1):
            if line.rstrip(" \t") != line:
                errors.append(f"{path.relative_to(ROOT)}:{number}: trailing whitespace")
            if "\t" in line:
                errors.append(f"{path.relative_to(ROOT)}:{number}: tab character; use spaces")
            if len(line) > MAX_LINE_LENGTH:
                errors.append(f"{path.relative_to(ROOT)}:{number}: line too long ({len(line)} > {MAX_LINE_LENGTH})")
if errors:
    print("FORMATTING=FAIL")
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print("FORMATTING=PASS: whitespace, indentation tabs, line endings, max line length")