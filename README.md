# Arc USDC Inspector

A lightweight, read-only CLI utility for inspecting public account data on Arc Testnet.

Built while exploring Arc's USDC-based network architecture.

## Features

- Connects to Arc Testnet through JSON-RPC
- Verifies the Arc Testnet chain ID
- Reads the latest block number
- Reads the native USDC balance of a public address
- Reads the ERC-20 USDC interface balance
- Compares native and ERC-20 USDC representations
- Validates EVM address formatting
- Requires no external Python packages

## Usage

```bash
python3 src/arc_inspector.py <public-address>
```

Example:

```bash
python3 src/arc_inspector.py 0x0000000000000000000000000000000000000001
```

Example output:

```text
Arc USDC Inspector
------------------
Address:          0x...
Chain ID:         5042002
Latest block:     ...
Native USDC:      ...
ERC-20 interface: ...
Representation:   matched ✓
Network:          Arc Testnet ✓
```

## Tests

Run the local unit tests with:

```bash
python3 -m unittest discover -s tests -v
```

## Security

This tool is intentionally read-only.

It does not:

- connect to a wallet
- request private keys or seed phrases
- sign messages
- sign transactions
- broadcast transactions
- request token approvals
- install third-party dependencies

Only public blockchain data is queried through Arc's JSON-RPC endpoint.

See `SECURITY.md` for additional notes.

## Requirements

- Python 3
- Internet connection for RPC queries

No additional packages are required.

## Project Structure

```text
arc-usdc-inspector/
├── src/
│   └── arc_inspector.py
├── tests/
│   └── test_arc_inspector.py
├── README.md
├── SECURITY.md
└── .gitignore
```

## Status

Early educational utility built for exploring Arc developer infrastructure.