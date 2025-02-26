from blockchain import Blockchain
from wallet import Wallet

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
