#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" return a list of documents in school having a specific topic"""
import pymongo


def schools_by_topic(mongo_collection, topic):
    """ return a list of documents in school having a specific topic"""
    return mongo_collection.find({"topics": topic})
