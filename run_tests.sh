#!/usr/bin/env bash

# Exit immediately if any command fails
set -e

# Activate virtual environment
source venv/Scripts/activate

# Run test suite
pytest
