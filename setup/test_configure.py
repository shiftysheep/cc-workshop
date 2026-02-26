"""Tests for configure.py AWS Bedrock setup script."""

import json
import sys
from pathlib import Path


# Add repo root to path so we can import configure.py as a module
REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))

import configure  # noqa: E402


def test_parse_sso_profiles_empty_file(tmp_path: Path) -> None:
    """Returns empty dict for empty/missing config."""
    empty_config = tmp_path / "config"
    empty_config.write_text("")

    result = configure.parse_sso_profiles(empty_config)

    assert result == {}


def test_parse_sso_profiles_extracts_sso_sections(tmp_path: Path) -> None:
    """Finds [profile X] with sso_start_url, returns correct dict."""
    config = tmp_path / "config"
    config.write_text("""[profile example.BedrockRole]
sso_start_url = https://example.awsapps.com/start
sso_region = us-west-2
region = us-west-2
output = json

[profile another.AdminRole]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
region = us-east-1
output = json
""")

    result = configure.parse_sso_profiles(config)

    assert len(result) == 2
    assert "example.BedrockRole" in result
    assert (
        result["example.BedrockRole"]["sso_start_url"]
        == "https://example.awsapps.com/start"
    )
    assert result["example.BedrockRole"]["region"] == "us-west-2"
    assert "another.AdminRole" in result


def test_parse_sso_profiles_ignores_non_sso_profiles(tmp_path: Path) -> None:
    """Skips profiles without sso_start_url."""
    config = tmp_path / "config"
    config.write_text("""[profile sso-profile]
sso_start_url = https://example.awsapps.com/start
sso_region = us-west-2
region = us-west-2

[profile legacy-profile]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
region = us-east-1
""")

    result = configure.parse_sso_profiles(config)

    assert len(result) == 1
    assert "sso-profile" in result
    assert "legacy-profile" not in result


def test_merge_settings_creates_new_file(tmp_path: Path) -> None:
    """Creates dir + file from scratch, writes correct JSON."""
    settings_path = tmp_path / ".claude" / "settings.json"

    result = configure.merge_settings(settings_path, "test.Profile", "us-west-2")

    assert settings_path.exists()
    assert settings_path.parent.exists()

    data = json.loads(settings_path.read_text())
    assert data["awsAuthRefresh"] == "aws sso login --profile ${AWS_PROFILE}"
    assert data["env"]["AWS_PROFILE"] == "test.Profile"
    assert data["env"]["AWS_REGION"] == "us-west-2"
    assert data["env"]["CLAUDE_CODE_USE_BEDROCK"] == "1"
    assert result == data


def test_merge_settings_includes_model_defaults(tmp_path: Path) -> None:
    """Verifies default model environment variables are set."""
    settings_path = tmp_path / ".claude" / "settings.json"

    configure.merge_settings(settings_path, "test.Profile", "us-west-2")

    data = json.loads(settings_path.read_text())
    assert (
        data["env"]["ANTHROPIC_DEFAULT_OPUS_MODEL"] == "us.anthropic.claude-opus-4-6-v1"
    )
    assert (
        data["env"]["ANTHROPIC_DEFAULT_HAIKU_MODEL"]
        == "us.anthropic.claude-haiku-4-5-20251001-v1:0"
    )
    assert (
        data["env"]["ANTHROPIC_DEFAULT_SONNET_MODEL"]
        == "us.anthropic.claude-sonnet-4-6"
    )


def test_merge_settings_preserves_existing_keys(tmp_path: Path) -> None:
    """Existing hooks, permissions survive the merge."""
    settings_path = tmp_path / ".claude" / "settings.json"
    settings_path.parent.mkdir(parents=True)

    existing = {
        "hooks": {"onSave": "ruff format"},
        "permissions": {"allowWrite": True},
        "customKey": "customValue",
        "env": {"OTHER_VAR": "preserved"},
    }
    settings_path.write_text(json.dumps(existing))

    result = configure.merge_settings(settings_path, "new.Profile", "us-east-1")

    assert result["hooks"] == {"onSave": "ruff format"}
    assert result["permissions"] == {"allowWrite": True}
    assert result["customKey"] == "customValue"
    assert result["env"]["OTHER_VAR"] == "preserved"
    assert result["env"]["AWS_PROFILE"] == "new.Profile"


def test_merge_settings_overwrites_bedrock_keys(tmp_path: Path) -> None:
    """Old AWS_PROFILE is replaced with new value."""
    settings_path = tmp_path / ".claude" / "settings.json"
    settings_path.parent.mkdir(parents=True)

    existing = {
        "awsAuthRefresh": "old command",
        "env": {
            "AWS_PROFILE": "old.Profile",
            "AWS_REGION": "old-region",
            "CLAUDE_CODE_USE_BEDROCK": "0",
        },
    }
    settings_path.write_text(json.dumps(existing))

    result = configure.merge_settings(settings_path, "new.Profile", "us-west-2")

    assert result["awsAuthRefresh"] == "aws sso login --profile ${AWS_PROFILE}"
    assert result["env"]["AWS_PROFILE"] == "new.Profile"
    assert result["env"]["AWS_REGION"] == "us-west-2"
    assert result["env"]["CLAUDE_CODE_USE_BEDROCK"] == "1"


def test_merge_settings_handles_malformed_json(tmp_path: Path) -> None:
    """Gracefully starts fresh on corrupt file."""
    settings_path = tmp_path / ".claude" / "settings.json"
    settings_path.parent.mkdir(parents=True)
    settings_path.write_text("{invalid json}")

    result = configure.merge_settings(settings_path, "test.Profile", "us-west-2")

    # Should create fresh config despite malformed input
    assert result["env"]["AWS_PROFILE"] == "test.Profile"
    assert result["awsAuthRefresh"] == "aws sso login --profile ${AWS_PROFILE}"
