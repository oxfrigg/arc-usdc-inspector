# Security Notes

## Scope

Arc USDC Inspector is a read-only educational utility.

It only queries public blockchain data from the Arc Testnet JSON-RPC endpoint.

## What the Tool Does

The tool can:

- validate a public EVM address
- read the current Arc chain ID
- read the latest block number
- read the native USDC balance of a public address

## What the Tool Does Not Do

The tool does not:

- connect to wallet extensions
- access private keys
- access seed phrases
- sign messages
- sign transactions
- broadcast transactions
- request approvals
- modify blockchain state
- read local wallet files
- execute code returned by the RPC server

## Dependency Policy

The project currently uses only Python standard-library modules.

No third-party Python packages are required.

This reduces dependency and supply-chain risk for this small educational utility.

## RPC Trust

The RPC endpoint is treated as an external data source.

Responses are parsed as JSON and are not executed as code.

The RPC provider may observe normal connection metadata such as the requesting IP address and queried public blockchain addresses.

## Development Approach

Security work in this repository follows a defensive approach:

read-only implementation → local tests → security documentation

No private keys, wallet secrets, vulnerable contracts, or exploit implementations are required.