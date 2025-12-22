# Test Plan for entryp Package

## Overview
This test suite demonstrates the behavior and trade-offs of the three execution modes in the `entryp` package.

## Test Structure

### Basic Tests (`test_basic.py`)
- Core decorator functionality
- Import vs main detection
- Basic mode switching
- All tests should pass

### Mode Comparison Tests
Each comparison highlights specific pros/cons of the different modes:

#### `test_mode_timing.py` ✅ (Implemented)
- **What it tests**: When each mode executes the decorated function
- **Key insight**: Shows execution order differences between immediate, at_exit, and first_rerun_remaining
- **Expected results**: All pass, demonstrating expected behavior

#### `test_mode_edge_cases.py` (Planned)
- **What it tests**: Variable availability, side effects, exception handling
- **Key insights**: 
  - IMMEDIATE: Can't access variables defined later (xfail)
  - AT_EXIT: Can access all variables (pass)
  - FIRST_RERUN_REMAINING: Potential side effects from code re-execution (xfail)
- **Expected results**: Mixed pass/xfail to highlight limitations

#### `test_mode_atexit.py` (Planned)
- **What it tests**: Integration with Python's atexit module
- **Key insights**:
  - AT_EXIT: Modifies atexit behavior, might break existing atexit handlers (xfail)
  - IMMEDIATE/FIRST_RERUN_REMAINING: Don't interfere with atexit (pass)
- **Expected results**: Mixed pass/xfail to highlight atexit complications

#### `test_mode_performance.py` (Planned)
- **What it tests**: Performance characteristics and overhead
- **Key insights**: 
  - IMMEDIATE: Minimal overhead (pass)
  - AT_EXIT: Slight overhead from atexit registration (pass)
  - FIRST_RERUN_REMAINING: Significant overhead from code re-execution (xfail for performance)

### Demo Scripts (`demos/` directory)
Real-world usage examples that tests execute as subprocesses:
- `simple_script.py`: Basic usage example
- `with_variables.py`: Shows variable access patterns
- `with_atexit.py`: Shows atexit integration issues
- `multiple_entrypoints.py`: Multiple decorated functions

### Test Utilities (`conftest.py`)
- `run_script()`: Execute Python scripts as subprocess
- `create_temp_module()`: Create temporary Python modules
- Pytest fixtures for clean test isolation

## Running Tests

```bash
# Run all tests
uv run pytest tests/

# Run specific test category
uv run pytest tests/test_mode_timing.py

# Run with verbose output to see xfail reasons
uv run pytest tests/ -v
```

## Understanding xfail Tests

Tests marked with `pytest.mark.xfail` are **expected to fail** and highlight limitations:
- They demonstrate trade-offs between different modes
- They document known limitations for users
- They help choose the right mode for specific use cases

## Test Philosophy

The tests serve dual purposes:
1. **Verification**: Ensure the decorator works as intended
2. **Documentation**: Show users the pros/cons of each mode through concrete examples
