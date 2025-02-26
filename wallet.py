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