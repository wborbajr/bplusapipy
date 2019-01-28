"""
aioHTTP Rest API
"""

from aiohttp import web

import sys
# sys.path.insert(0, '/blockchain')
sys.path.append('../')
from blockchain import Blockchain

from uuid import uuid4

import json


async def handle(request):
    response_obj = { 'status' : 'success' }
    return web.Response(text=json.dumps(response_obj))


def mine(request):

    # Generate a globally unique address for this node
    node_identifier = str(uuid4()).replace('-', '')

    # Instantiate the Blockchain
    blockchain = Blockchain()

    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return web.json_response(response), 200


async def new_transaction(request):
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


async def full_chain(request):
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


async def register_nodes(request):
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


async def consensus(request):
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


def init():
    app = web.Application()

    app.router.add_get('/', handle)
    app.router.add_get('/mine', mine)
    app.router.add_post('/transactions/new', new_transaction)
    app.router.add_get('/chain', full_chain)
    app.router.add_post('/nodes/register', register_nodes)
    app.router.add_get('/nodes/resolve', consensus)

    return app

# if __name__ == '__main__':
web.run_app(init(), port=3000)
