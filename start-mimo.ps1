Get-Content .env | ForEach-Object {
    if ($_ -match '^\s*([^#][^=]+)=(.+)$') {
        [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim(), "Process")
    }
}

$env:ANTHROPIC_BASE_URL = "https://token-plan-cn.xiaomimimo.com/anthropic"
$env:ANTHROPIC_API_KEY = $env:MIMO_API_KEY
$env:ANTHROPIC_MODEL = "mimo-v2.5-pro"
claude