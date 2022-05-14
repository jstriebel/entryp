# main-entrypoint

A decorator to avoid `if __name__ == "__main__":`

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
