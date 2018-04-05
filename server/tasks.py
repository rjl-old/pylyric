"""
Contains tasks that will be loaded by the asyncio loop
when the server is started. Load any tasks that should
be run async into the tasks list, which is imported and
added to the server's event loop.
"""
import asyncio
from typing import Callable


def async_run_every(seconds: int) -> Callable:
    """
    A decorator that wraps a function call in an asyncio wait
    and ensures it is run infinitely no more than once every
    n seconds.
    :param seconds: The number of seconds.
    :return: A new async function.
    """
    def decorator(func: Callable) -> Callable:
        async def new_func(*args, **kwargs):
            while True:
                func(*args, **kwargs)
                await asyncio.sleep(seconds)

        new_func.__name__ = func.__name__
        new_func.__doc__ = func.__doc__

        return new_func
    return decorator


@async_run_every(5)
def notify_me():
    print("it's been 5 sec")


tasks = [
    notify_me
]
