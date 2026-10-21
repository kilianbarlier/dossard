#!/usr/bin/env python3
"""Hook PreToolUse : bloque les commandes shell destructrices."""

import json
import re
import sys

SHELLS = {"Bash", "PowerShell"}

RM_OPTIONS = re.compile(r"\brm\b((?:\s+-[^\s;&|]+)+)")
GIT_PUSH_FORCE = re.compile(
    r"\bgit\b[^;&|\n]*\bpush\b[^;&|\n]*"
    r"(?:\s--force(?![-\w])|\s-[A-Za-z]*f[A-Za-z]*(?=\s|$))"
)
DROP = re.compile(r"\bDROP\s+(?:TABLE|VIEW)\b", re.IGNORECASE)


def rm_rf(command: str) -> bool:
    for match in RM_OPTIONS.finditer(command):
        options = match.group(1).split()
        short = "".join(o[1:] for o in options if not o.startswith("--"))
        recursive = "r" in short.lower() or "--recursive" in options
        force = "f" in short or "--force" in options
        if recursive and force:
            return True
    return False


def raison(command: str) -> str | None:
    if rm_rf(command):
        return "rm -rf"
    if GIT_PUSH_FORCE.search(command):
        return "git push --force"
    if DROP.search(command):
        return "DROP TABLE / DROP VIEW"
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    if not isinstance(payload, dict) or payload.get("tool_name") not in SHELLS:
        return 0
    tool_input = payload.get("tool_input")
    command = tool_input.get("command") if isinstance(tool_input, dict) else None
    if not isinstance(command, str):
        return 0
    motif = raison(command)
    if motif:
        print(f"Bloqué par le hook garde.py : {motif}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
