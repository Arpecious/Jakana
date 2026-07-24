param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string] $File
)

$env:PYTHONPATH = Join-Path $PSScriptRoot "src"
python -m jakana.cli run $File
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
