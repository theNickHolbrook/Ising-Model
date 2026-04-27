# Ising Model — compile, simulate, encode, clean up
# Run from the directory containing super_fast_2d.cpp
# Usage: powershell -ExecutionPolicy Bypass -File .\run.ps1

$ErrorActionPreference = "Stop"

# ── 1. Compile ────────────────────────────────────────────────────────────────
Write-Host "`nCompiling..." -ForegroundColor Cyan
g++ -O2 -static -o ising wicked_fast_2d.cpp
if ($LASTEXITCODE -ne 0) {
    Write-Host "Compilation failed." -ForegroundColor Red
    exit 1
}
Write-Host "Compiled OK." -ForegroundColor Green

# ── 2. Run simulation ─────────────────────────────────────────────────────────
Write-Host "`nRunning simulation..." -ForegroundColor Cyan
.\ising.exe
if ($LASTEXITCODE -ne 0) {
    Write-Host "Simulation failed (exit code $LASTEXITCODE)." -ForegroundColor Red
    exit 1
}
Write-Host "Simulation complete." -ForegroundColor Green

# ── 3. Encode video ───────────────────────────────────────────────────────────
Write-Host "`nEncoding video..." -ForegroundColor Cyan

if (Test-Path "ising.mp4") { Remove-Item "ising.mp4" }

ffmpeg -framerate 30 -i frames/frame_%05d.bmp -c:v libx264 -pix_fmt yuv420p ising.mp4
if ($LASTEXITCODE -ne 0) {
    Write-Host "ffmpeg encoding failed." -ForegroundColor Red
    exit 1
}
Write-Host "Video saved to ising.mp4" -ForegroundColor Green

# ── 4. Clean up frames ────────────────────────────────────────────────────────
Write-Host "`nCleaning up frames..." -ForegroundColor Cyan
Remove-Item -Path "frames\*" -Force
Remove-Item -Path "frames" -Force
Write-Host "Frames deleted." -ForegroundColor Green

Write-Host "`nAll done!" -ForegroundColor Green
