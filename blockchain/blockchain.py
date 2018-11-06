import datetime
import hashlib
import json
from urllib.parse import urlparse

import requests


class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.nodes = set()
        self.create_block(proof=1, previous_hash="0")

    @property
    def length(self):
        return len(self.chain)

    def create_block(self, proof, previous_hash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "proof": proof,  # Nonce
            "previous_hash": previous_hash,
            "transactions": self.transactions,
        }
        self.transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = self.calculate_hash_operation(new_proof, previous_proof)
            if hash_operation[:4] == "0000":
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def calculate_hash_operation(self, new_proof, previous_proof):
        calc = new_proof ** 2 - previous_proof ** 2
        return hashlib.sha256(str(calc).encode()).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while len(chain) > block_index:
            block = chain[block_index]

            if not self._validate_block_hash(previous_block, block):
                return False

            if not self._validate_block_proof(previous_block, block):
                return False

            block_index += 1
            previous_block = block

        return True

    def add_transaction(self, sender, receiver, amount):
        self.transactions.append(
            {"sender": sender, "receiver": receiver, "amount": amount}
        )

        previous_block = self.get_previous_block()
        return previous_block["index"] + 1

    def add_node(self, address):
        url = urlparse(address)
        self.nodes.add(url.netloc)

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = self.length

        for node in network:
            response = requests.get(f"http://{node}/get_chain")

            if response.ok:
                data = response.json()
                if data["length"] > max_length and self.is_chain_valid(data["chain"]):
                    max_length = data["length"]
                    longest_chain = data["chain"]

        if longest_chain:
            self.chain = longest_chain
            return True
        return False

    def _validate_block_hash(self, prev, cur):
        return cur["previous_hash"] == self.hash(prev)

    def _validate_block_proof(self, prev, cur):
        previous_proof = prev["proof"]
        proof = cur["proof"]
        hash_operation = self.calculate_hash_operation(proof, previous_proof)
        return hash_operation[:4] == "0000"
