#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Union, Optional, Callable
import redis


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(self._redis.incr("count"))
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        data = self._redis.get(key)
        if fn is not None:
            data = fn(data)
        return data

    def get_str(self, key: str) -> str:
        return self.get(key, fn=str)

    def get_int(self, key: str) -> int:
        return self.get(key, fn=int)
