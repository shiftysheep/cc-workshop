# AWS Bedrock configuration

## Automated Setup (Recommended)

Run the automated configuration script:

```shell
uv run setup/configure.py
```

The script will:
1. Check for existing Bedrock configuration
2. Install aws-sso-util if needed
3. Populate SSO profiles (or use existing ones)
4. Let you select a profile interactively
5. Write the complete settings.json configuration

Options:
- `--sso-region TEXT` - AWS SSO region (will prompt if not provided)
- `--sso-url TEXT` - AWS SSO start URL (will prompt if not provided)
- `--refresh` - Force refresh of SSO profiles even if they exist

To test the configuration script:

```shell
uv run --with pytest --with typer --with textual pytest setup/test_configure.py -v
```

## Manual Setup

If you prefer to configure manually:

### Configure AWS SSO Profiles

- Install aws-sso-util with UV
```shell
uv tool install aws-sso-util
```
- Populate the SSO configuration:
```shell
aws-sso-util configure populate --sso-region <SSO_REGION> -u <AWS_SSO_URL> --region <SSO_REGION>`
```
## Find your SSO profile name

After populating, check your AWS config file for the profile name to use:

- macOS / Linux (WSL): `~/.aws/config`
- Windows: `C:\Users\<your_user>\.aws\config`

Look for a section like `[profile YourOrg.RoleName]` — that profile name is what you'll set as `AWS_PROFILE` below.

## Configure Claude Code to use Amazon Bedrock

Configure claude to utilize this profile by creating/updating the following settings.json:

- MacOS or Linux (WSL): `~/.claude/settings.json`
- Windows: `C:\Users\<your_user>\.claude\`

```json
{
  "awsAuthRefresh": "aws sso login --profile ${AWS_PROFILE}",
  "env": {
    "AWS_REGION": "<SSO_REGION>",
    "AWS_PROFILE": "<CHANGE TO THE AWS PROFILE YOU WOULD LIKE TO USE FOR BEDROCK>",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "us.anthropic.claude-opus-4-6-v1",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "us.anthropic.claude-haiku-4-5-20251001-v1:0",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "us.anthropic.claude-sonnet-4-6",
    "CLAUDE_CODE_USE_BEDROCK": "1",
  }
}
```
