# statusline.ps1
# Windows/PowerShell statusline for Claude Code.
# Claude Code pipes JSON session data to stdin; this script writes one line to stdout.
# Install: copy to ~\.claude\statusline.ps1
# Settings: { "statusLine": { "type": "command", "command": "pwsh -NoProfile -File $env:USERPROFILE\\.claude\\statusline.ps1" } }

param()

# Read all stdin and parse JSON
$json  = $input | Out-String | ConvertFrom-Json
$model = if ($json.model.display_name) { $json.model.display_name } else { 'claude' }
$pct   = if ($null -ne $json.context_window.used_percentage) { [int]$json.context_window.used_percentage } else { 0 }
$rawDir = if ($json.workspace.current_dir) { $json.workspace.current_dir } else { (Get-Location).Path }

# Abbreviate path: replace home with ~, truncate deep paths to .../ or ...\ last two parts
# $env:USERPROFILE is Windows; $env:HOME covers macOS/Linux — fall back gracefully
$homeDir = if ($env:USERPROFILE) { $env:USERPROFILE } else { $env:HOME }
$display = $rawDir
if ($homeDir -and $display.StartsWith($homeDir)) { $display = '~' + $display.Substring($homeDir.Length) }
$sep   = [System.IO.Path]::DirectorySeparatorChar
$parts = $display -split [regex]::Escape($sep)
$cwd   = if ($parts.Length -gt 3) { '...' + $sep + ($parts[-2..-1] -join $sep) } else { $display }

# Git info (omitted if not in a repo or git is unavailable)
# Use -C $rawDir so git operates on the workspace path, not the script's cwd
$gitPart = ''
if (Get-Command git -ErrorAction SilentlyContinue) {
    git -C $rawDir rev-parse --git-dir 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) {
        $branch  = git -C $rawDir branch --show-current 2>$null
        $dirty   = git -C $rawDir status --porcelain 2>$null
        $state   = if ($dirty) { 'modified' } else { 'clean' }
        $gitPart = " | $state | $branch"
    }
}

Write-Output "$model | $pct% context | $cwd$gitPart"
