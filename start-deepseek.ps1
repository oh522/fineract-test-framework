Get-Content .env | ForEach-Object {
    if ($_ -match '^\s*([^#][^=]+)=(.+)$') {
        [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim(), "Process")
    }
}

$env:ANTHROPIC_BASE_URL = "https://api.deepseek.com"
$env:ANTHROPIC_API_KEY = $env:DEEPSEEK_API_KEY
$env:ANTHROPIC_MODEL = "deepseek-chat"
claude