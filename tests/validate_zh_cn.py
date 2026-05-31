#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
FRONTEND_ZH_CN = ROOT / "resources" / "frontend-zh-CN.json"

CODE_KEYWORDS = (
    "claude code",
    "code session",
    "code review",
    "github",
    "repository",
    "repositories",
    "workspace",
    "terminal",
    "pull request",
    "branch",
)

MANAGED_SETTINGS_KEYWORDS = (
    "inference configuration",
    "inference gateway",
    "gateway credential",
    "credential kind",
    "credential source",
    "static api key",
    "view changelog",
    "apply changes",
    "custom inference headers",
    "gateway base url",
    "gateway api key",
    "gateway auth scheme",
)

REQUIRED_FRONTEND_TEXTS = (
    "High-contrast dark theme",
    "Use a darker, near-black background when dark mode is on.",
    "Interface font",
    "Transcript text size",
    "Dynamic workflows",
    "Let Claude run multiple agents in parallel for complex tasks. Workflows can use a lot of your usage limit quickly.",
    "Cowork files",
    "Your artifacts and scheduled tasks are stored at {path}.",
    "Enable the Cowork tab. Claude works on longer tasks like research, analysis, and documents.",
    "Enable the Code tab. Claude writes and runs code.",
    "These apply regardless of which surfaces are enabled.",
    "Hostnames the agent's tools may reach from the Cowork and Code tabs. Also surfaced under Egress Requirements.",
    "Built-in tools removed from Cowork.",
    'Per-tool approval policy. "ask" requires user approval before each call; "allow" is the default. Use Disabled built-in tools to remove a tool entirely.',
    "Add policy",
    "Collapse sidebar",
    "Change",
    "Customize",
)

VARIABLE_RE = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)(?=[},])")
TAG_RE = re.compile(r"</?([A-Za-z][A-Za-z0-9]*)\b[^>]*>")


def load_json(path: Path) -> dict[str, str]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise AssertionError(f"{path} must contain a JSON object")
    return data


def find_claude_install_location() -> Path | None:
    override = os.environ.get("CLAUDE_APP_INSTALL_LOCATION")
    if override:
        return Path(override)

    if os.name != "nt":
        return None

    result = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            "(Get-AppxPackage -Name Claude -ErrorAction SilentlyContinue).InstallLocation",
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    location = result.stdout.strip().splitlines()
    return Path(location[0]) if location else None


def frontend_en_us_path() -> Path:
    install_location = find_claude_install_location()
    if not install_location:
        raise AssertionError(
            "Set CLAUDE_APP_INSTALL_LOCATION to a Claude install path to run this validation."
        )
    path = install_location / "app" / "resources" / "ion-dist" / "i18n" / "en-US.json"
    if not path.exists():
        raise AssertionError(f"Cannot find Claude frontend en-US.json: {path}")
    return path


def has_code_keyword(text: str) -> bool:
    lowered = text.lower()
    return any(keyword in lowered for keyword in CODE_KEYWORDS + MANAGED_SETTINGS_KEYWORDS)


def required_frontend_text_keys(en: dict[str, str]) -> list[str]:
    required: list[str] = []
    missing_texts: list[str] = []
    for text in REQUIRED_FRONTEND_TEXTS:
        matches = [key for key, value in en.items() if str(value) == text]
        if not matches:
            missing_texts.append(text)
            continue
        required.extend(matches)
    if missing_texts:
        sample = "\n".join(f"  {text}" for text in missing_texts)
        raise AssertionError(f"Cannot find required frontend source texts in en-US.json:\n{sample}")
    return sorted(set(required))


def placeholders(text: str) -> set[str]:
    variables = {f"{{{name}}}" for name in VARIABLE_RE.findall(text)}
    tags = {f"<{name}>" for name in TAG_RE.findall(text)}
    return variables | tags


def main() -> int:
    en = load_json(frontend_en_us_path())
    zh = load_json(FRONTEND_ZH_CN)

    required_keys = sorted(
        set(key for key, value in en.items() if has_code_keyword(str(value)))
        | set(required_frontend_text_keys(en))
    )
    missing = [key for key in required_keys if key not in zh]
    if missing:
        sample = "\n".join(f"  {key}: {en[key]}" for key in missing[:30])
        raise AssertionError(
            f"frontend-zh-CN.json is missing {len(missing)} Claude Code / managed settings related keys.\n{sample}"
        )

    placeholder_errors: list[str] = []
    for key in required_keys:
        if "??" in str(zh[key]):
            placeholder_errors.append(f"{key}: contains replacement question marks")
        source_placeholders = placeholders(str(en[key]))
        target_placeholders = placeholders(str(zh[key]))
        missing_placeholders = source_placeholders - target_placeholders
        if missing_placeholders:
            placeholder_errors.append(
                f"{key}: missing placeholders {sorted(missing_placeholders)}"
            )

    if placeholder_errors:
        sample = "\n".join(f"  {line}" for line in placeholder_errors[:30])
        raise AssertionError(f"Placeholder mismatches in Claude Code / managed settings zh-CN strings:\n{sample}")

    print(f"Validated {len(required_keys)} Claude Code / managed settings related zh-CN frontend strings.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
