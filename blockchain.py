# Module 1 - Create a Blockchain
import datetime
import hashlib
import json

from flask import Flask, jsonify

# Part 1 - Building a Blockchain


class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash="0")


# Part 2 - Mining our Blockchain
