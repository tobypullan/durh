# blockchain.py
import hashlib
import time
import json

class Block:
    def __init__(self, timestamp, transactions, previous_hash=""):
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        block_string = json.dumps({
            "timestamp": self.timestamp,
            "transactions": [t.to_dict() for t in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        
        return hashlib.sha256(block_string).hexdigest()
    
    def mine_block(self, difficulty):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        
        print(f"Block mined: {self.hash}")


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4
        self.pending_transactions = []
        self.mining_reward = 100
    
    def create_genesis_block(self):
        return Block(time.time(), [], "0")
    
    def get_latest_block(self):
        return self.chain[-1]
    
    def mine_pending_transactions(self, mining_reward_address):
        # Create mining reward transaction
        reward_transaction = Transaction(None, mining_reward_address, self.mining_reward)
        self.pending_transactions.append(reward_transaction)
        
        # Create new block
        block = Block(time.time(), self.pending_transactions, self.get_latest_block().hash)
        block.mine_block(self.difficulty)
        
        # Add block to chain
        self.chain.append(block)
        self.pending_transactions = []
    
    def add_transaction(self, transaction):
        if not transaction.sender or not transaction.recipient:
            return False
        
        if not transaction.is_valid():
            return False
        
        self.pending_transactions.append(transaction)
        return True
    
    def get_balance(self, address):
        balance = 0
        
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == address:
                    balance -= transaction.amount
                if transaction.recipient == address:
                    balance += transaction.amount
        
        return balance
    
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Check hash
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check previous hash
            if current_block.previous_hash != previous_block.hash:
                return False
            
            # Validate all transactions
            for transaction in current_block.transactions:
                if not transaction.is_valid():
                    return False
        
        return True


# transaction.py
import hashlib
import json
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = time.time()
        self.signature = None
    
    def calculate_hash(self):
        transaction_string = json.dumps({
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp
        }, sort_keys=True).encode()
        
        return hashlib.sha256(transaction_string).hexdigest()
    
    def sign_transaction(self, private_key):
        if self.sender is None:  # Mining reward
            return
        
        transaction_hash = self.calculate_hash().encode()
        
        signature = private_key.sign(
            transaction_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        self.signature = signature
    
    def is_valid(self):
        if self.sender is None:  # Mining reward
            return True
        
        if not self.signature:
            return False
        
        transaction_hash = self.calculate_hash().encode()
        
        try:
            public_key = serialization.load_pem_public_key(self.sender.encode())
            public_key.verify(
                self.signature,
                transaction_hash,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            return False
    
    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "signature": self.signature.hex() if self.signature else None
        }


# wallet.py
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

class Wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.generate_key_pair()
    
    def generate_key_pair(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        
        self.public_key = self.private_key.public_key()
    
    def get_public_key_string(self):
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()
    
    def create_transaction(self, recipient, amount, blockchain):
        balance = blockchain.get_balance(self.get_public_key_string())
        
        if balance < amount:
            print("Not enough balance!")
            return None
        
        transaction = Transaction(self.get_public_key_string(), recipient, amount)
        transaction.sign_transaction(self.private_key)
        
        return transaction


# network.py (Basic structure)
import socket
import threading
import json

class P2PServer:
    def __init__(self, blockchain, port=5000):
        self.blockchain = blockchain
        self.port = port
        self.nodes = set()
    
    def start_server(self):
        # Basic server setup
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', self.port))
        server.listen(5)
        
        while True:
            client, address = server.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client,))
            client_thread.start()
    
    def handle_client(self, client):
        # Basic message handling
        pass
    
    def broadcast_transaction(self, transaction):
        # Send to all nodes
        pass
    
    def broadcast_block(self, block):
        # Send to all nodes
        pass
    
    def add_node(self, address):
        self.nodes.add(address)


# main.py (Example usage)
if __name__ == "__main__":
    # Create blockchain
    my_blockchain = Blockchain()
    
    # Create wallets
    wallet1 = Wallet()
    wallet2 = Wallet()
    
    # Generate a transaction
    transaction = wallet1.create_transaction(wallet2.get_public_key_string(), 10, my_blockchain)
    my_blockchain.add_transaction(transaction)
    
    # Mine block
    my_blockchain.mine_pending_transactions(wallet1.get_public_key_string())
    
    # Check balances
    print(f"Wallet 1 balance: {my_blockchain.get_balance(wallet1.get_public_key_string())}")
    print(f"Wallet 2 balance: {my_blockchain.get_balance(wallet2.get_public_key_string())}")
