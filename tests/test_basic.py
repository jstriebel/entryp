"""
Basic functionality tests for the entryp package.
These tests verify core decorator behavior and should all pass.
"""
from .conftest import run_script


def test_basic_decorator_functionality(mode):
    """
    Test that the decorator works as a basic replacement for if __name__ == '__main__'.
    Test all three modes for basic functionality.
    """
    script = f'''
import entryp

@entryp.oint(mode="{mode}")
def main():
    print("Hello from main")

print("Module loaded")
'''
    
    # Test as main - should execute both
    stdout = run_script(script)
    assert "Module loaded" in stdout, f"Mode {mode} didn't load module"
    assert "Hello from main" in stdout, f"Mode {mode} didn't execute main"
    
    # Test as import - should only load module
    stdout = run_script(script, as_main=False)
    assert "Module loaded" in stdout, f"Mode {mode} didn't load module on import"
    assert "Hello from main" not in stdout, f"Mode {mode} executed main on import"


def test_multiple_entrypoints_execution_order(mode):
    """Test that multiple entrypoints execute in definition order for all modes."""
    script = f'''
import entryp

@entryp.oint(mode="{mode}")
def first():
    print("First function")

@entryp.oint(mode="{mode}")
def second():
    print("Second function")

@entryp.oint(mode="{mode}")
def third():
    print("Third function")
'''
    stdout = run_script(script)
    lines = stdout.strip().split('\n')
    assert lines == [
        "First function",
        "Second function",
        "Third function",
    ]


def test_decorator_without_parentheses():
    """Test that the decorator works without parentheses."""
    script = f'''
import entryp

@entryp.oin
def main():
    print("Hello")
'''
    
    stdout = run_script(script)
    assert f"Hello" in stdout


def test_decorator_without_args():
    """Test that the decorator works without arguments."""
    script = f'''
import entryp

@entryp.oint()
def main():
    print("Hello")
'''
    
    stdout = run_script(script)
    assert f"Hello" in stdout


def test_renamed_decorator():
    """Test that the decorator works without parentheses."""
    script = f'''
from entryp import entrypoint

@entrypoint
def main():
    print("Hello")
'''
    
    stdout = run_script(script)
    assert f"Hello" in stdout


def test_decorator_returns_original_function():
    """Test that the decorator returns the original function unchanged."""
    script = '''
import entryp

@entryp.oint
def main():
    return "test_value"

if __name__ == "__main__":
    print("Original function name:", main.__name__)
    print("Original function callable:", callable(main))
'''
    
    stdout = run_script(script)
    assert "Original function name: main" in stdout
    assert "Original function callable: True" in stdout
