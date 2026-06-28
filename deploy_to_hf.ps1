# ============================================================
# deploy_to_hf.ps1
# Deploy hr-analytics-gaming to HuggingFace Spaces
#
# USAGE (from the hr-analytics-gaming repo root):
#   .\deploy_to_hf.ps1 -HfUser remichenouri
#
# PRE-REQUISITE: Create the Space first on huggingface.co
#   Owner      : remichenouri
#   Space name : hr-analytics-gaming
#   SDK        : Streamlit
#   Visibility : Public
# ============================================================

param(
    [string]$HfUser    = "remichenouri",
    [string]$SpaceName = "hr-analytics-gaming",
    [string]$SpaceDir  = "$env:TEMP\hf-$SpaceName"
)

$ErrorActionPreference = "Stop"
$RepoRoot  = $PSScriptRoot
$AppSource = Join-Path $RepoRoot "app"
$HfUrl     = "https://huggingface.co/spaces/$HfUser/$SpaceName"

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host " HuggingFace Spaces Deployment" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host " Space : $HfUrl"
Write-Host " Source: $AppSource"
Write-Host " Target: $SpaceDir"
Write-Host ""

# ── Step 1 : Clone or update the Space ────────────────────────────────────────
if (Test-Path $SpaceDir) {
    Write-Host "[1/5] Space folder exists — pulling latest..." -ForegroundColor Yellow
    git -C $SpaceDir pull
} else {
    Write-Host "[1/5] Cloning Space from HuggingFace..." -ForegroundColor Yellow
    git clone $HfUrl $SpaceDir
}

# ── Step 2 : Clean previous app files (keep .git) ─────────────────────────────
Write-Host "[2/5] Cleaning old files..." -ForegroundColor Yellow
Get-ChildItem $SpaceDir -Exclude ".git" | Remove-Item -Recurse -Force

# ── Step 3 : Copy app/ content to Space root ──────────────────────────────────
Write-Host "[3/5] Copying app/ files to Space root..." -ForegroundColor Yellow
Copy-Item -Path "$AppSource\*" -Destination $SpaceDir -Recurse -Force

# ── Step 4 : Put the HuggingFace README in place ──────────────────────────────
Write-Host "[4/5] Writing HuggingFace README.md..." -ForegroundColor Yellow
$HfReadmeSrc = Join-Path $RepoRoot "HF_README_hr_analytics_gaming.md"
Copy-Item -Path $HfReadmeSrc -Destination (Join-Path $SpaceDir "README.md") -Force

# ── Step 5 : Commit & push ────────────────────────────────────────────────────
Write-Host "[5/5] Committing and pushing to HuggingFace..." -ForegroundColor Yellow
Set-Location $SpaceDir

git add .

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
git commit -m "deploy: hr-analytics-gaming ($timestamp)" --allow-empty

git push

Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host " DONE — app is live at:" -ForegroundColor Green
Write-Host " $HfUrl" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""
Write-Host "HuggingFace builds take 2-3 minutes."
Write-Host "Watch the build logs at: $HfUrl (tab 'App' -> 'Build logs')"

Set-Location $RepoRoot
