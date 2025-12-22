#!/usr/bin/env bash

# Test runner script for the entryp package

set -e

echo "Running tests for entryp package..."

# Install the package in development mode
echo "Installing package in development mode..."
uv pip install -e .

# Run the tests
echo "Running pytest..."
uv run pytest tests/ -v

echo "Running format check..."
uv run ruff format --check

echo "Running linting..."
uv run ruff check

echo "Running type checking..."
uv run mypy entryp

echo "All tests and checks passed!"
