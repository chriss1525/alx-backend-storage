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
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> str:
        """get data from redis"""
        data = self._redis.get(key)
        if fn:
            data = fn(data)
        return data

    def get_str(self, key: str) -> str:
        """get string data from redis"""
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """get int data from redis"""
        return self.get(key, int)
