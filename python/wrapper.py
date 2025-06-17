"""
This module contains various decorators that can be used to modify the behaviour of functions.

Decorators are a powerful feature in Python that allow you to wrap a function with
another function, adding functionality before and/or after the wrapped function is called.
"""

import functools
import time


# basic decorator example (use as boilerplate)
def decorator(func):
    """A simple decorator that wraps a function"""

    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        # Do something before
        value = func(*args, **kwargs)
        # Do something after
        return value

    return wrapper_decorator


def slow_down(func):
    """Sleep 1 second before calling the function"""

    @functools.wraps(func)
    def wrapper_slow_down(*args, **kwargs):
        time.sleep(1)
        return func(*args, **kwargs)

    return wrapper_slow_down


def timer(func):
    """Print the runtime of the decorated function"""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value

    return wrapper_timer


# @timer
# def waste_some_time(num_times):
#     for _ in range(num_times):
#         sum([i**2 for i in range(10000)])


def repeat(_func=None, *, num_times=2):
    """Run the decorated function num_times times"""

    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper_repeat(*args, **kwargs):
            for _ in range(num_times):
                value = func(*args, **kwargs)
            return value

        return wrapper_repeat

    if _func is None:
        return decorator_repeat

    return decorator_repeat(_func)


def debug(func):
    """Print the function signature and return value"""

    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")
        return value

    return wrapper_debug


# register a function just to make it available for use later (acts like a subset of globals())
PLUGINS = {}


def register(func):
    """Register a function as a plug-in"""
    PLUGINS[func.__name__] = func
    return func


def test_register():
    """Test the register decorator"""

    @register
    def say_hello(name):
        return f"Hello {name}"

    @register
    def be_awesome(name):
        return f"Yo {name}, together we are the best!"

    def randomly_greet(name):
        import random

        greeter, greeter_func = random.choice(list(PLUGINS.items()))
        print(f"Using {greeter!r}")
        return greeter_func(name)

    print(randomly_greet("Alice"))
