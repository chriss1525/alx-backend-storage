#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Union, Optional, Callable
import redis
from functools import wraps


def call_history(method: Callable) -> Callable:
    """ Decorator to store the history of inputs and outputs for a particular"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper function to store the history of inputs and outputs for a particular"""
        name = method.__qualname__
        input_key = name + ":inputs"
        output_key = name + ":outputs"

        input_value = str(args)
        self._redis.rpush(input_key, input_value)

        output_value = str(method(self, *args, **kwargs))

        self._redis.rpush(output_key, output_value)

        return output_value
    return wrapper


def count_calls(method: Callable) -> Callable:
    """ Decorator to count the number of times a function has been called"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper function to count the number of times a function has been called"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def replay(self, method: Callable) -> None:
    """ Display the history of calls of a particular function"""
    name = method.__qualname__
    inputs_key = name + ":inputs"
    outputs_key = name + ":outputs"

    count = self.__redis.lrange(inputs_key, 0, -1)
    values = self.__redis.lrange(outputs_key, 0, -1)

    call_count = len(count)
    print(f"{name} was called {call_count} times:")
    for i in range(call_count):
        input_args = count[i]
        output_value = values[i]
        print(f"{name}(*{input_args}) -> {output_value}")


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(self._redis.incr("count"))
        self._redis.set(key, data)
        return key

    def get(self,
            key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        data = self._redis.get(key)
        if fn is not None:
            data = fn(data)
        return data

    def get_str(self, key: str) -> str:
        return self.get(key, fn=str)

    def get_int(self, key: str) -> int:
        return self.get(key, fn=int)
