#!/usr/bin/env pwsh
# UV integration runner — Windows counterpart to uv_run_all.sh (PR 5)
# Usage: .\uv_run_all.ps1

$ErrorActionPreference = "Stop"
$ProjectDir = $PSScriptRoot
Set-Location $ProjectDir

Write-Host "================================================================"
Write-Host " 11-DIMENSIONAL UNIVERSE SIMULATION - UV INTEGRATION TEST"
Write-Host "================================================================"
Write-Host ""

Write-Host "UV version:"
uv --version
Write-Host ""

Write-Host "----------------------------------------------------------------"
Write-Host " TEST 1: Pytest harness (unit + integration, not slow)"
Write-Host "----------------------------------------------------------------"
uv run pytest tests/ -m "not slow" --tb=short
Write-Host ""

Write-Host "----------------------------------------------------------------"
Write-Host " TEST 2: Normalized parity compare (legacy_dual)"
Write-Host "----------------------------------------------------------------"
uv run python -m simulation_11.parity compare --baseline legacy_dual
Write-Host ""

Write-Host "----------------------------------------------------------------"
Write-Host " TEST 3: CLI help smoke"
Write-Host "----------------------------------------------------------------"
uv run simulation-11 --help | Out-Null
Write-Host "CLI help OK"
Write-Host ""

Write-Host "================================================================"
Write-Host " ALL UV INTEGRATION TESTS COMPLETED"
Write-Host "================================================================"