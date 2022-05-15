# main-entrypoint

[![PyPI version](https://img.shields.io/pypi/v/main-entrypoint)](https://pypi.python.org/pypi/main-entrypoint)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/main-entrypoint.svg)](https://pypi.python.org/pypi/main-entrypoint)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A decorator to avoid `if __name__ == "__main__":`, instead use

```python
from main_entrypoint import entrypoint

@entrypoint
def main():
    print("Hello World")
```

```bash
$ python my_script.py
Hello World

$ python -c "import my_script"
# no output
```


## Installation

```bash
pip install main-entrypoint
```


## Details

Specifying the `@entrypoint` decorator on a function `my_func` can be considered equivalent to running
```python
if __name__ == "__main__":
    my_func()
```
at the end of the same module.

If the decorator is used multiple times in the same file, the functions are executed in the order they are defined.

The default `entrypoint` decorator uses the [`atexit` module](https://docs.python.org/library/atexit.html). Simple usage of registered atexit functions still works as expected, but involved workflows (e.g. specific exception-flows) relying on atexit behaviour might:tm: break. In those cases, please consider to use one of the two other available modes, `first_rerun_remaining` and `immediate`, e.g.

```python
from main_entrypoint import entrypoint

@entrypoint(mode="immediate")
def main():
    print("Hello World")
```

`immediate` calls the decorated function immediately, entities defined later in the module will not be available, so moving the function to the end of the module is encouraged. `first_rerun_remaining` will effectively run everything after the decorated function twice, so the code should be free of side-effects and preferably only consist of definitions in this case. The default mode is `at_exit` and should be considered as a first choice.

## Future Work

- [ ] tests
- [ ] automating formatting, checking and releases
- [ ] allow to pass arguments to the entrypoint function


## License

[MIT](LICENSE)
