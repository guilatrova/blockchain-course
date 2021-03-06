import sys
from uuid import uuid4

from flask import Flask, jsonify, request

from blockchain import Blockchain

app = Flask(__name__)

node_address = str(uuid4()).replace("-", "")

blockchain = Blockchain()
port = sys.argv[1] if len(sys.argv) > 1 else 5000
sender_map = {5000: "Goku", 5001: "Krillin"}
sender = sender_map.get(port, "Latrova")


@app.route("/mine_block", methods=["GET"])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block["proof"]
    previous_hash = blockchain.hash(previous_block)

    proof = blockchain.proof_of_work(previous_proof)

    blockchain.add_transaction(node_address, sender, 1)
    new_block = blockchain.create_block(proof, previous_hash)

    response = {"message": "Congratulations, new proof: " + str(new_block["proof"])}
    response.update(new_block)

    return jsonify(response), 200


@app.route("/get_chain", methods=["GET"])
def get_chain():
    response = {"chain": blockchain.chain, "length": blockchain.length}
    return jsonify(response), 200


@app.route("/chain/status", methods=["GET"])
def is_valid():
    response = {"valid": blockchain.is_chain_valid(blockchain.chain)}
    return jsonify(response), 200


@app.route("/add_transaction", methods=["POST"])
def add_transaction():
    json = request.get_json()
    transaction_keys = ["sender", "receiver", "amount"]
    if not all(key in json for key in transaction_keys):
        return "Key missing", 400

    index = blockchain.add_transaction(**json)
    response = {"message": f"This transaction will be added to Block {index}"}
    return jsonify(response), 201


@app.route("/connect_node", methods=["POST"])
def connect_node():
    json = request.get_json()
    nodes = json.get("nodes", False)

    if nodes:
        for node in nodes:
            blockchain.add_node(node)

        response = {
            "message": f"All nodes are now connected. Blockchain contains {len(nodes)} nodes",
            "total_nodes": list(blockchain.nodes),
        }
        return jsonify(response), 201

    return "No node", 400


@app.route("/chain/replace", methods=["GET"])
def replace_chain():
    response = {"replaced": blockchain.replace_chain(), "chain": blockchain.chain}
    return jsonify(response), 200


app.run(host="0.0.0.0", port=port)
