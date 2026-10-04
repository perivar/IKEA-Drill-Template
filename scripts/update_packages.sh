#!/bin/bash

# Script to update Python packages and regenerate requirements.txt
# Installs CadQuery and dependencies for parametric 3D CAD modeling

# Exit on any error
set -e

# Source shared package utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/packages_utils.sh"

# Function to update all packages
update_packages() {
    ensure_pip

    echo ""
    echo "Step 1: Installing CadQuery and OCP (Open CASCADE)..."
    pip install cadquery

    echo ""
    echo "Step 2: Installing development utilities..."
    pip install jupyter ipykernel

    echo ""
    echo "Step 3: Installing lint and type-check tools (ruff, pyright)..."
    pip install ruff pyright

    echo ""
    echo "Step 5: Verifying CadQuery installation (may take ~60s on first import)..."
    python -c "import cadquery; print(f'CadQuery {cadquery.__version__} installed successfully')"

    echo ""
    echo "Step 6: Verifying lint and type-check tools..."
    ruff --version
    pyright --version

    echo ""
    echo "Step 7: Regenerating requirements.txt..."
    pip freeze --all > requirements.txt
    echo "requirements.txt has been regenerated."

    echo ""
    echo "Package update completed!"
}

# Main execution
echo "Starting package update process for KitchenAid 5KSB555 Coupler..."

# Navigate to the project root directory
cd "$SCRIPT_DIR/.."

# Check for Python version and set up virtual environment
check_python
setup_venv

# Perform the updates
update_packages

echo ""
echo "========================================================"
echo "  Update Completed Successfully!"
echo "  requirements.txt has been regenerated with current versions"
echo "========================================================"
