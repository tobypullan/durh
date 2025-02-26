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