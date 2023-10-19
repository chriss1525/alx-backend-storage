#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import redis
import requests

r = redis.Redis()

def get_page(url: str) -> str:
    count = f"count:{url}"

    if r.exists(count):
        r.incr(count)
    else:
        r.setex(count, 10, 1)

    cached_contet = r.get(url)
    if cached_contet:
        return cached_contet.decode('utf-8')

    resp = requests.get(url)
    content = resp.text

    r.setex(url, 10, content)

    return content

if __name__ == '__main__':
    url = "http://slowwly.robertomurray.co.uk"
    page_content = get_page(url)
    print(page_content)
