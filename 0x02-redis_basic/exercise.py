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
        self._redis.set(key, data)
        return key
