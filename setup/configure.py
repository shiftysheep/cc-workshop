#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "typer",
#     "textual",
# ]
# ///
# mypy: disable-error-code="no-untyped-def, no-untyped-call"
"""Automate AWS Bedrock setup for Claude Code workshop participants."""

import configparser
import json
import shutil
import subprocess  # nosec B404
from pathlib import Path
from typing import cast

import typer  # type: ignore[import-not-found]
from textual.app import App  # type: ignore[import-not-found]
from textual.widgets import OptionList  # type: ignore[import-not-found]
from textual.widgets.option_list import Option  # type: ignore[import-not-found]

# Constants
CLAUDE_DIR = Path.home() / ".claude"
SETTINGS_PATH = CLAUDE_DIR / "settings.json"
AWS_CONFIG_PATH = Path.home() / ".aws" / "config"

BEDROCK_ENV: dict[str, str] = {
    "AWS_REGION": "",  # Set dynamically
    "AWS_PROFILE": "",  # Set dynamically
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "us.anthropic.claude-opus-4-6-v1",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "us.anthropic.claude-haiku-4-5-20251001-v1:0",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "us.anthropic.claude-sonnet-4-6",
    "CLAUDE_CODE_USE_BEDROCK": "1",
}

BEDROCK_ENV_KEYS = {
    "awsAuthRefresh": "aws sso login --profile ${AWS_PROFILE}",
    "env": BEDROCK_ENV,
}

app = typer.Typer()


def parse_sso_profiles(config_path: Path) -> dict[str, dict[str, str]]:
    """Parse AWS config file and extract SSO profiles.

    Returns dict mapping profile names to their config values.
    Only includes profiles with sso_start_url.
    """
    if not config_path.exists():
        return {}

    parser = configparser.ConfigParser()
    try:
        parser.read(config_path)
    except configparser.Error:
        return {}

    profiles = {}
    for section in parser.sections():
        # Extract profile name (sections are like "profile example.Role")
        if section.startswith("profile "):
            profile_name = section.replace("profile ", "")
        elif section == "default":
            profile_name = "default"
        else:
            continue

        # Only include profiles with sso_start_url
        if parser.has_option(section, "sso_start_url"):
            profiles[profile_name] = dict(parser.items(section))

    return profiles


class ProfileSelector(App[str]):  # type: ignore[misc]
    """Textual app for selecting an AWS SSO profile."""

    def __init__(self, profiles: list[str]):
        super().__init__()
        self.profiles = profiles

    def compose(self):
        """Create the option list with profiles."""
        options = [Option(profile) for profile in self.profiles]
        yield OptionList(*options)

    def on_option_list_option_selected(self, event) -> None:
        """Handle profile selection."""
        self.exit(result=str(event.option.prompt))


def merge_settings(settings_path: Path, profile: str, region: str):
    """Merge Bedrock config into existing settings.json or create new.

    Preserves all existing keys, overwrites Bedrock-specific keys.
    Returns the final settings dict.
    """
    # Load existing settings or start fresh
    existing = {}
    if settings_path.exists():
        try:
            existing = json.loads(settings_path.read_text())
        except json.JSONDecodeError:
            # Malformed JSON - start fresh
            existing = {}

    # Deep merge: preserve existing keys, overwrite Bedrock keys
    merged = existing.copy()
    merged["awsAuthRefresh"] = BEDROCK_ENV_KEYS["awsAuthRefresh"]

    # Merge env dict specifically
    if "env" not in merged:
        merged["env"] = {}

    bedrock_env = BEDROCK_ENV.copy()
    bedrock_env["AWS_PROFILE"] = profile
    bedrock_env["AWS_REGION"] = region

    merged["env"].update(bedrock_env)

    # Ensure parent directory exists
    settings_path.parent.mkdir(parents=True, exist_ok=True)

    # Write settings
    settings_path.write_text(json.dumps(merged, indent=2))

    return merged


def install_aws_sso_util() -> None:
    """Ensure aws-sso-util is installed via uv tool."""
    if shutil.which("aws-sso-util"):
        typer.echo("✓ aws-sso-util already installed")
        return

    typer.echo("Installing aws-sso-util...")
    result = subprocess.run(  # nosec B603 B607
        ["uv", "tool", "install", "aws-sso-util"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        typer.echo(f"Error installing aws-sso-util: {result.stderr}", err=True)
        raise typer.Exit(code=1)

    typer.echo("✓ aws-sso-util installed")


def populate_sso_config(sso_region: str, sso_url: str) -> None:
    """Run aws-sso-util configure populate."""
    typer.echo(f"Populating SSO config for {sso_url}...")

    result = subprocess.run(  # nosec B603 B607
        [
            "aws-sso-util",
            "configure",
            "populate",
            "--sso-region",
            sso_region,
            "-u",
            sso_url,
            "--region",
            sso_region,
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        typer.echo(f"Error populating SSO config: {result.stderr}", err=True)
        raise typer.Exit(code=1)

    typer.echo("✓ SSO config populated")


def check_existing_config() -> None:
    """Check for existing Bedrock config and prompt for reconfiguration."""
    if not SETTINGS_PATH.exists():
        return

    try:
        settings = json.loads(SETTINGS_PATH.read_text())
        env = settings.get("env", {})
        if env.get("CLAUDE_CODE_USE_BEDROCK") == "1":
            typer.echo("Existing Bedrock configuration found:")
            typer.echo(f"  AWS_PROFILE: {env.get('AWS_PROFILE', 'not set')}")
            typer.echo(f"  AWS_REGION: {env.get('AWS_REGION', 'not set')}\n")

            if not typer.confirm("Reconfigure?", default=False):
                typer.echo("Keeping existing configuration.")
                raise typer.Exit()
    except json.JSONDecodeError:
        pass


def refresh_sso_profiles(
    sso_region: str | None, sso_url: str | None
) -> dict[str, dict[str, str]]:
    """Install aws-sso-util, populate config, and return profiles."""
    install_aws_sso_util()

    actual_sso_region: str = sso_region or typer.prompt("AWS SSO region")
    actual_sso_url: str = sso_url or typer.prompt("AWS SSO start URL")

    populate_sso_config(actual_sso_region, actual_sso_url)

    # Re-parse profiles
    profiles = parse_sso_profiles(AWS_CONFIG_PATH)
    if not profiles:
        typer.echo("Error: No SSO profiles found after populate", err=True)
        raise typer.Exit(code=1)

    return profiles


def select_profile(profile_names: list[str]) -> str:
    """Select profile from list (auto-select if only one, otherwise prompt)."""
    if len(profile_names) == 1:
        selected_profile = profile_names[0]
        typer.echo(f"\nAuto-selecting only profile: {selected_profile}")
        return selected_profile

    typer.echo(f"\nFound {len(profile_names)} profiles. Select one:\n")
    for i, name in enumerate(profile_names, 1):
        typer.echo(f"  {i}. {name}")
    typer.echo()

    # Launch Textual profile selector
    selector = ProfileSelector(profile_names)
    return cast(str, selector.run())


@app.command()  # type: ignore[untyped-decorator]
def main(
    sso_region: str = typer.Option(None, help="AWS SSO region"),
    sso_url: str = typer.Option(None, help="AWS SSO start URL"),
    refresh: bool = typer.Option(False, help="Force refresh of SSO profiles"),
):
    """Configure AWS Bedrock for Claude Code workshop."""
    typer.echo("AWS Bedrock Setup for Claude Code\n")

    check_existing_config()

    # Check for existing SSO profiles
    profiles = parse_sso_profiles(AWS_CONFIG_PATH)

    if profiles and not refresh:
        typer.echo(f"Found {len(profiles)} existing SSO profile(s)")
    elif profiles and refresh:
        typer.echo(f"Found {len(profiles)} existing SSO profile(s), refreshing...")
        profiles = refresh_sso_profiles(sso_region, sso_url)
    else:
        typer.echo("No SSO profiles found, setting up...")
        profiles = refresh_sso_profiles(sso_region, sso_url)

    # Profile selection
    selected_profile = select_profile(list(profiles.keys()))
    selected_region = profiles[selected_profile].get(
        "region", sso_region or "us-west-2"
    )

    # Write settings.json
    typer.echo(f"\nConfiguring Claude Code for profile: {selected_profile}")
    final_settings = merge_settings(SETTINGS_PATH, selected_profile, selected_region)

    # Step 8: Print confirmation
    typer.echo(f"\n✓ Configuration written to {SETTINGS_PATH}\n")
    typer.echo("Environment variables set:")
    for key, value in final_settings["env"].items():
        typer.echo(f"  {key}: {value}")

    typer.echo(f"\nawsAuthRefresh: {final_settings['awsAuthRefresh']}\n")
    typer.echo("Setup complete! Restart Claude Code to use Bedrock.")


if __name__ == "__main__":
    app()
