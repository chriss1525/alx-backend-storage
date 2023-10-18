#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Union
import redis

"""basic redis manipulation"""


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """store data in redis"""
        key = str(self._redis.incr("count"))
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """get data from redis"""
        data = self._redis.get(key)
        if fn is not None:
            data = fn(data)
        return data

    def get_str(self, key: str) -> str:
        """get string data from redis"""
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """get int data from redis"""
        return self.get(key, int)
