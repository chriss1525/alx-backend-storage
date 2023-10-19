#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" create a cache system with redis """
import redis
import requests

r = redis.Redis()


def get_page(url: str) -> str:
    """ get page """
    count  = 0
    
    r.set(f"count:{url}", count)
    resp = requests.get(url)
    r.incr(f"count:{url}")
    r.setex(f"cached: {url}", 10, r.get(f"cached: {url}"))
    return resp.text
