import atexit
import inspect
from enum import Enum, unique
from functools import partial
from typing import Any, Callable, Optional, TypeVar, Union, overload

from typing_extensions import ParamSpec

_T = TypeVar("_T")
_P = ParamSpec("_P")


_entrypoint_stack = []


def _add_to_entrypoint_stack(func: Callable[[], Any]) -> None:
    _entrypoint_stack.append(func)


def _run_entrypoint_stack() -> None:
    for func in _entrypoint_stack:
        func()


_exit_stack = []


def _add_to_exit_stack(
    func: Callable[_P, _T], *args: _P.args, **kwargs: _P.kwargs
) -> Callable[_P, _T]:
    _exit_stack.append(partial(func, *args, **kwargs))
    return func


def _run_exit_stack() -> None:
    for func in _exit_stack[::-1]:
        func()


@unique
class EntrypointMode(Enum):
    AT_EXIT = "at_exit"
    FIRST_RERUN_REMAINING = "first_rerun_remaining"
    IMMEDIATE = "immediate"


_F = TypeVar("_F", bound=Callable)


@overload
def entrypoint(
    func: _F, *, mode: Union[EntrypointMode, str] = EntrypointMode.AT_EXIT
) -> _F:
    ...


@overload
def entrypoint(
    func: None, *, mode: Union[EntrypointMode, str] = EntrypointMode.AT_EXIT
) -> Callable[[_F], _F]:
    ...


def entrypoint(
    func: Optional[_F] = None,
    *,
    mode: Union[EntrypointMode, str] = EntrypointMode.AT_EXIT
) -> Union[_F, Callable[[_F], _F]]:
    mode = EntrypointMode(mode)

    if func is not None and not callable(func):
        mode = func
        func = None

    if func is None:
        return partial(entrypoint, mode=mode)

    current_frame = inspect.currentframe()
    assert current_frame is not None
    calling_frame = current_frame.f_back
    if calling_frame is None:
        return func
    calling_module = inspect.getmodule(calling_frame)
    if calling_module is None:
        return func
    if calling_module.__name__ == "__main__":
        if mode == EntrypointMode.IMMEDIATE:
            func()
        elif mode == EntrypointMode.AT_EXIT:
            if len(_entrypoint_stack) == 0:
                atexit.register(_run_exit_stack)
                atexit.register(_run_entrypoint_stack)
                atexit.register = _add_to_exit_stack
            _add_to_entrypoint_stack(func)
        elif mode == EntrypointMode.FIRST_RERUN_REMAINING:
            source = inspect.getsource(calling_module)
            f_source, f_start = inspect.getsourcelines(func)
            f_end = f_start - 1 + len(f_source)  # f_start is 1-indexed
            remaining_source = "".join(source.splitlines(keepends=True)[f_end:])
            exec(remaining_source, calling_frame.f_globals, calling_frame.f_locals)
            func()
    return func
