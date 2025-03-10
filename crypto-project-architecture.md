# Cryptocurrency Project Architecture

## Core Components

1. **Blockchain Module**
   - Manages the chain of blocks
   - Handles consensus and chain validation
   - Manages block mining

2. **Transaction Module**
   - Handles creation and validation of transactions
   - Manages transaction pool
   - Includes signature verification

3. **Wallet Module**
   - Manages key pairs for users
   - Handles wallet creation and recovery
   - Tracks balances

4. **Networking Module**
   - Manages peer-to-peer communications
   - Synchronizes blockchain across nodes
   - Broadcasts transactions and blocks

5. **User Interface**
   - Command-line interface or simple web interface
   - Wallet interactions
   - Transaction creation and viewing

## Suggested Team Split

### Team Member 1: Core Blockchain & Transactions
- Blockchain implementation
- Transaction management
- Mining algorithm
- Consensus mechanism

### Team Member 2: Wallet, Networking & Interface
- Wallet functionality
- Network communication
- User interface
- Node synchronization

## Class Structure and Responsibilities

### Blockchain Module
```
- Block Class
  - Stores transactions
  - Contains hash, previous hash, timestamp, nonce
  - Methods: calculate_hash(), validate()

- Blockchain Class
  - Stores chain of blocks
  - Methods: add_block(), validate_chain(), replace_chain(), mine_block()
```

### Transaction Module
```
- Transaction Class
  - Contains sender, recipient, amount, signature
  - Methods: calculate_hash(), sign(), verify_signature()

- TransactionPool Class
  - Manages pending transactions
  - Methods: add_transaction(), validate_transaction(), get_transactions()
```

### Wallet Module - Toby
```
- Wallet Class
  - Manages key pairs
  - Methods: generate_keys(), calculate_balance(), create_transaction()

- KeyPair Class
  - Stores public and private keys
  - Methods: sign(), verify()
```

### Networking Module
```
- Node Class
  - Represents a node in the network
  - Methods: broadcast(), connect(), sync()

- P2PServer Class
  - Manages connections to other nodes
  - Methods: listen(), broadcast_transaction(), broadcast_block()
```

### User Interface Module
```
- CLI Class or WebInterface Class
  - Handles user input/output
  - Methods: display_menu(), show_balance(), create_transaction()
```

## Suggested Development Steps

1. Start with core classes (Block, Transaction, Wallet)
2. Implement blockchain validation and mining
3. Add transaction pool and validation
4. Implement networking and synchronization
5. Create user interface
6. Testing and optimization
