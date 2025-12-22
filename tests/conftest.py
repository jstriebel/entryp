import os
import subprocess
import sys
import tempfile

import pytest


@pytest.fixture(params=["immediate", "at_exit", "first_rerun_remaining"])
def mode(request):
    """Fixture that provides all three execution modes."""
    return request.param


def run_script(script_content: str, as_main: bool = True) -> str:
    """
    Run a Python script and return stdout and return code.

    Args:
        script_content: The Python code to execute
        as_main: If True, run as __main__, if False, import the module

    Returns:
        stdout
    """
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.py',
        delete=False
    ) as temp_file:
        temp_file.write(script_content)
        temp_file_path = temp_file.name
    try:

        if as_main:
            # Run the script directly
            result = subprocess.run(
                [sys.executable, temp_file_path],
                capture_output=True,
                text=True,
                check=True,
            )
        else:
            # Import the module instead
            module_dir = os.path.dirname(temp_file_path)
            module_name = os.path.basename(temp_file_path)[:-3]  # Remove .py

            import_cmd = (
                f'import sys; '
                f'sys.path.insert(0, "{module_dir}"); '
                f'import {module_name}'
            )

            result = subprocess.run(
                [sys.executable, '-c', import_cmd],
                capture_output=True,
                text=True,
                check=True,
            )

        return result.stdout

    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
