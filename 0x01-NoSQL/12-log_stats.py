#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Provide some stats about nginx logs stored in MongoDB"""

from pymongo import MongoClient

def log_stats():
    """Provides some stats about nginx logs stored in MongoDB"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs = client.logs.nginx

    # Count the total number of documents
    total_logs = logs.count_documents({})

    print(f"{total_logs} logs")

    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        # Count the number of documents for each method
        method_count = logs.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")

    # Count the number of documents with method=GET and path=/status
    status_check_count = logs.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")

    # Close the MongoDB client
    client.close()

if __name__ == "__main__":
    log_stats()

