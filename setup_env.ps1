<#
Setup PowerShell script to create a Python 3.11 virtual environment and install dependencies.
Run from project root (PowerShell):
  .\setup_env.ps1

If you have the Python launcher installed, this uses `py -3.11` to create the venv.
If you don't have Python 3.11, install it from https://www.python.org/downloads/windows/
#>

Write-Host "Checking for Python 3.11..."
$pyExe = ""
try {
    & py -3.11 --version > $null 2>&1
    $pyExe = "py -3.11"
} catch {
    try {
        & python --version > $null 2>&1
        $pyExe = "python"
    } catch {
        Write-Error "Python not found. Install Python 3.11 and re-run this script."
        exit 1
    }
}

Write-Host "Creating virtual environment .venv using $pyExe..."
& $pyExe -m venv .venv

Write-Host "Activating virtual environment..."
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
. .\ .venv\Scripts\Activate.ps1

Write-Host "Upgrading pip and wheel..."
python -m pip install --upgrade pip wheel

Write-Host "Installing dependencies from requirements.txt (may take a few minutes)..."
python -m pip install -r requirements.txt

Write-Host "Installing CPU build of torch and torchvision (recommended on systems without CUDA)..."
python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

Write-Host "Setup complete. Activate the venv with: .\.venv\Scripts\Activate.ps1 and then run: python main_integrated.py"
