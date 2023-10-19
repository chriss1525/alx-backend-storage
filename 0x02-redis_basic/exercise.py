#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" simple class with basic redis """
from typing import Union, Optional, Callable
import redis
from functools import wraps


def call_history(method: Callable) -> Callable:
    """ store the history of inputs and outputs for a particular function"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wrapper function"""
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
    """counts how many times methods of the Cache class are called"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wrapper function"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def replay(method: Callable) -> None:
    """Displays the history of calls of a particular function"""
    method_key = method.__qualname__
    inputs, outputs = method_key + ':inputs', method_key + ':outputs'
    redis = method.__self__._redis
    method_count = redis.get(method_key).decode('utf-8')
    print(f'{method_key} was called {method_count} times:')
    IOTuple = zip(redis.lrange(inputs, 0, -1), redis.lrange(outputs, 0, -1))
    for inp, outp in list(IOTuple):
        attr, data = inp.decode("utf-8"), outp.decode("utf-8")
        print(f'{method_key}(*{attr}) -> {data}')


class Cache:
    """ Cache class"""

    def __init__(self):
        """ constructor"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ store data"""
        key = str(self._redis.incr("count"))
        self._redis.set(key, data)
        return key

    def get(self,
            key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """ get data"""
        data = self._redis.get(key)
        if fn is not None:
            data = fn(data)
        return data

    def get_str(self, key: str) -> str:
        """ get string"""
        return self.get(key, fn=str)

    def get_int(self, key: str) -> int:
        """ get int"""
        return self.get(key, fn=int)
