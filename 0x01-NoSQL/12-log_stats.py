#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" provide some stats about nginx logs stored in MongoDB"""

from pymongo import MongoClient


def log_stats():
    """ provides some stats about nginx logs stored in MongoDB"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs = client.logs.nginx
    print("{} logs".format(logs.count_documents({})))
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        print("\tmethod {}: {}".format(
            method, logs.count_documents({"method": method})))
    print("{} status check".format(logs.count_documents(
        {"method": "GET", "path": "/status"})))
    print("IPs:")
    ips = logs.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    for ip in ips:
        print("\t{}: {}".format(ip.get("_id"), ip.get("count")))
    print("404 status code: {}".format(
        logs.count_documents({"status_code": 404})))
    client.close()

if __name__ == "__main__":
    log_stats()
