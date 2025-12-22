"""
Tests that highlight the pros and cons of different execution modes.
Each test demonstrates specific behaviors, edge cases, and potential issues.
"""
import os
import subprocess
import sys
import tempfile


class TestModeComparison:
    """Tests that reveal the behavioral differences between execution modes."""

    def _run_script(self, script_content: str, as_main: bool = True):
        """Helper to run a script and capture output."""
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.py'
        ) as f:
            f.write(script_content)
            script_path = f.name

        try:
            if as_main:
                result = subprocess.run(
                    [sys.executable, script_path],
                    capture_output=True,
                    text=True
                )
            else:
                # Import the module instead of running as __main__
                module_name = os.path.basename(script_path)[:-3]  # Remove .py
                import_cmd = (
                    f'import sys; '
                    f'sys.path.insert(0, "{os.path.dirname(script_path)}"); '
                    f'import {module_name}'
                )
                result = subprocess.run([
                    sys.executable, '-c', import_cmd
                ], capture_output=True, text=True)

            return result.stdout, result.stderr, result.returncode
        finally:
            os.unlink(script_path)

    def test_execution_timing_differences(self):
        """
        Demonstrates when each mode executes the decorated function.
        
        PROS/CONS highlighted:
        - IMMEDIATE: Executes right away, can't access later variables
        - AT_EXIT: Executes at exit, can access all variables
        - FIRST_RERUN_REMAINING: Executes immediately + reruns remaining code
        """
        
        # IMMEDIATE mode - executes right away
        immediate_script = '''
import entryp

print("1. Script starting")

@entryp.oint(mode="immediate")
def main():
    print("2. Main function executed")

print("3. Script continuing after decorator")
print("4. Script ending")
'''
        
        # AT_EXIT mode - executes at program exit
        at_exit_script = '''
import entryp

print("1. Script starting")

@entryp.oint(mode="at_exit")
def main():
    print("4. Main function executed")

print("2. Script continuing after decorator")
print("3. Script ending")
'''
        
        # FIRST_RERUN_REMAINING mode - executes immediately, then reruns remaining
        first_rerun_script = '''
import entryp

print("1. Script starting")

@entryp.oint(mode="first_rerun_remaining")
def main():
    print("2. Main function executed")

print("3. Script continuing after decorator")
print("4. Script ending")
'''
        
        immediate_out, _, _ = self._run_script(immediate_script)
        at_exit_out, _, _ = self._run_script(at_exit_script)
        first_rerun_out, _, _ = self._run_script(first_rerun_script)
        
        # Verify execution order
        assert (
            "1. Script starting\n2. Main function executed\n3. Script continuing"
            in immediate_out
        )
        assert (
            "1. Script starting\n2. Script continuing\n3. Script ending\n"
            "4. Main function executed" in at_exit_out
        )
        assert (
            "1. Script starting\n2. Main function executed\n3. Script continuing\n"
            "4. Script ending" in first_rerun_out
        )

    def test_variable_availability_issues(self):
        """
        Shows how IMMEDIATE mode can't access variables defined later.
        
        PROS/CONS highlighted:
        - IMMEDIATE: CON - Can't access variables defined after decorator
        - AT_EXIT: PRO - Can access all variables defined in the module
        """
        
        # IMMEDIATE mode - CONS: Can't access variables defined after decorator
        immediate_script = '''
import entryp

@entryp.oint(mode="immediate")
def main():
    try:
        print(f"Message: {message}")
    except NameError:
        print("ERROR: message not defined yet")

message = "Hello World"
'''
        
        # AT_EXIT mode - PROS: Can access all variables
        at_exit_script = '''
import entryp

@entryp.oint(mode="at_exit")
def main():
    print(f"Message: {message}")

message = "Hello World"
'''
        
        immediate_out, _, _ = self._run_script(immediate_script)
        at_exit_out, _, _ = self._run_script(at_exit_script)
        
        assert "ERROR: message not defined yet" in immediate_out
        assert "Message: Hello World" in at_exit_out

    def test_import_vs_main_behavior(self):
        """
        Verifies that all modes properly respect __name__ == "__main__".
        
        PROS/CONS highlighted:
        - All modes: PRO - Properly respect __name__ == "__main__" convention
        - All modes: PRO - Don't execute when imported
        """
        
        for mode in ["immediate", "at_exit", "first_rerun_remaining"]:
            script = f'''
import entryp

@entryp.oint(mode="{mode}")
def main():
    print("Main executed in {mode} mode")

print("Module loaded")
'''
            
            # Test as main
            main_out, _, _ = self._run_script(script)
            assert "Main executed" in main_out
            assert "Module loaded" in main_out
            
            # Test as import
            import_out, _, _ = self._run_script(script, as_main=False)
            assert "Main executed" not in import_out
            assert "Module loaded" in import_out


if __name__ == "__main__":
    # Simple test runner for manual verification
    test_instance = TestModeComparison()
    test_instance.test_execution_timing_differences()
    print("Basic test passed - use 'uv run pytest' to run all tests")
