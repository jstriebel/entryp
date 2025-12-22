"""
Mode timing comparison tests for the entryp package.
These tests demonstrate when each mode executes and highlight timing differences.
"""
from .conftest import run_script


def test_immediate_mode_timing():
    """Test that immediate mode executes right away during decoration."""
    script = '''
import entryp

print("1. Script starting")

@entryp.oint(mode="immediate")
def main():
    print("2. Main function executed")

print("3. Script continuing after decorator")
print("4. Script ending")
'''
    
    stdout = run_script(script)
    
    lines = stdout.strip().split('\n')
    assert "1. Script starting" in lines[0]
    assert "2. Main function executed" in lines[1]
    assert "3. Script continuing after decorator" in lines[2]
    assert "4. Script ending" in lines[3]


def test_at_exit_mode_timing():
    """Test that at_exit mode executes at program exit."""
    script = '''
import entryp

print("1. Script starting")

@entryp.oint(mode="at_exit")
def main():
    print("4. Main function executed")

print("2. Script continuing after decorator")
print("3. Script ending")
'''
    
    stdout = run_script(script)
    
    lines = stdout.strip().split('\n')
    assert "1. Script starting" in lines[0]
    assert "2. Script continuing after decorator" in lines[1]
    assert "3. Script ending" in lines[2]
    assert "4. Main function executed" in lines[3]


def test_first_rerun_remaining_mode_timing():
    """Test that first_rerun_remaining mode executes immediately then reruns remaining code."""
    script = '''
import entryp

print("1. Script starting")

@entryp.oint(mode="first_rerun_remaining")
def main():
    print("2. Main function executed")

print("3. Script continuing after decorator")
print("4. Script ending")
'''
    
    stdout = run_script(script)
    
    lines = stdout.strip().split('\n')
    assert "1. Script starting" in lines[0]
    assert "2. Main function executed" in lines[1]
    assert "3. Script continuing after decorator" in lines[2]
    assert "4. Script ending" in lines[3]


def test_mode_timing_comparison():
    """Compare execution timing across all modes for documentation purposes."""
    modes_and_expected_order = [
        ("immediate", ["1. Script starting", "2. Main executed", "3. Script continuing"]),
        ("at_exit", ["1. Script starting", "2. Script continuing", "3. Main executed"]),
        ("first_rerun_remaining", ["1. Script starting", "2. Main executed", "3. Script continuing"]),
    ]
    
    for mode, expected_order in modes_and_expected_order:
        script = f'''
import entryp

print("1. Script starting")

@entryp.oint(mode="{mode}")
def main():
    print("2. Main executed")

print("3. Script continuing")
'''
        
        stdout = run_script(script)

        
        lines = stdout.strip().split('\n')
        for i, expected_line in enumerate(expected_order):
            assert expected_line in lines[i], f"Mode {mode} failed timing test"
