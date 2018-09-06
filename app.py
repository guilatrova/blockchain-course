# Module 1 - Create a Blockchain

from flask import Flask, jsonify

from .blockchain import Blockchain

# Part 2 - Mining our Blockchain

app = Flask(__name__)

blockchain = Blockchain()


@app.route("/mine_block", methods=["GET"])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block["proof"]
    previous_hash = blockchain.hash(previous_block)

    proof = blockchain.proof_of_work(previous_proof)

    new_block = blockchain.create_block(proof, previous_hash)

    response = {"message": "Congratulations, new proof: " + new_block["proof"]}
    response.update(new_block)

    return jsonify(response), 200
