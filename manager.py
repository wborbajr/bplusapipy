"""
Manager
"""

from blockchain import Blockchain
from uuid import uuid4


# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

if __name__ == '__main__':
    from app import app
