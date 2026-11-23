#!/usr/bin/env python3
"""Add Gemini.app's bundled agy as a local ACP provider in T3 Code."""

import argparse
import json
import os
from pathlib import Path
import stat
import tempfile

PROVIDER_ID = "gemini-app-agy"
PROVIDER_NAME = "Gemini.app agy (Local ACP)"
DEFAULT_AGY = Path("/Applications/Gemini.app/Contents/Helpers/agy")


def add_provider(settings_path, agy_path):
    if not agy_path.is_file() or not os.access(agy_path, os.X_OK):
        raise ValueError(f"agy is not executable at {agy_path}")

    original = settings_path.read_bytes()
    settings = json.loads(original)
    if not isinstance(settings, dict):
        raise ValueError("T3 settings must contain a JSON object.")
    providers = settings.setdefault("providerInstances", {})
    if not isinstance(providers, dict):
        raise ValueError("providerInstances must be a JSON object.")

    command = {"source": "local", "commandPath": str(agy_path), "commandArgs": ["acp"]}
    if PROVIDER_ID in providers:
        existing = providers[PROVIDER_ID]
        config = existing.get("config") if isinstance(existing, dict) else None
        if (
            isinstance(config, dict)
            and existing.get("driver") == "acpRegistry"
            and all(config.get(key) == value for key, value in command.items())
        ):
            print(f"{PROVIDER_NAME} is already configured. Enable it in T3 if it is disabled.")
            return
        raise ValueError(f"Provider ID {PROVIDER_ID!r} is in use with different settings.")

    providers[PROVIDER_ID] = {
        "driver": "acpRegistry",
        "displayName": PROVIDER_NAME,
        "enabled": True,
        "config": command,
    }

    mode = stat.S_IMODE(settings_path.stat().st_mode)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=settings_path.parent, prefix=".t3-gemini-acp-",
        delete=False,
    ) as temporary:
        temporary_path = Path(temporary.name)
        try:
            os.fchmod(temporary.fileno(), mode)
            json.dump(settings, temporary, ensure_ascii=False, indent=2)
            temporary.write("\n")
            temporary.close()
            if settings_path.read_bytes() != original:
                raise ValueError("T3 settings changed during this operation. Run the command again.")
            os.replace(temporary_path, settings_path)
        finally:
            temporary_path.unlink(missing_ok=True)

    print(f"Added {PROVIDER_NAME}. Refresh provider status in T3.")


def main():
    t3_home = Path(os.environ.get("T3CODE_HOME") or Path.home() / ".t3")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--settings", type=Path, default=t3_home / "userdata/settings.json",
                        help="Path to T3 Code's settings.json")
    parser.add_argument("--agy", type=Path, default=DEFAULT_AGY,
                        help="Path to the executable shipped inside Gemini.app")
    args = parser.parse_args()

    try:
        settings_path = args.settings.expanduser().resolve()
        agy_path = args.agy.expanduser().absolute()
        add_provider(settings_path, agy_path)
    except (OSError, ValueError) as error:
        parser.exit(1, f"{parser.prog}: {error}\n")


if __name__ == "__main__":
    main()
