#!/bin/bash

# Script to ensure a virtual environment exists and install packages from requirements.txt

# Exit on any error
set -e

# Source shared package utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/packages_utils.sh"

# Function to install packages
install_packages() {
    # Check if requirements.txt exists
    if [ ! -f "requirements.txt" ]; then
        echo "Error: requirements.txt not found in the current directory"
        exit 1
    fi

    ensure_pip
    
    echo "Installing packages from requirements.txt..."
    pip install -r requirements.txt
}

# Main execution
echo "Starting package installation process for KitchenAid 5KSB555 Coupler..."

# Navigate to the project root directory
cd "$SCRIPT_DIR/.."

# Check for Python version and set up virtual environment
check_python
setup_venv

# Install packages
install_packages

echo "Package installation completed!"
echo "Current package list:"
pip list

echo ""
echo "========================================================"
echo "  Setup Finished Successfully!"
echo "========================================================"
