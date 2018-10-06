from uuid import uuid4

from flask import Flask, jsonify

from blockchain import Blockchain

app = Flask(__name__)

node_address = str(uuid4()).replace("-", "")

blockchain = Blockchain()


@app.route("/mine_block", methods=["GET"])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block["proof"]
    previous_hash = blockchain.hash(previous_block)

    proof = blockchain.proof_of_work(previous_proof)

    blockchain.add_transaction(node_address, "Latrova", 1)
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


app.run(host="0.0.0.0", port=5000)
