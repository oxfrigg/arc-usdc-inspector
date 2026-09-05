import json
import re
import sys
import urllib.error
import urllib.request


RPC_URL = "https://rpc.testnet.arc.network"
EXPECTED_CHAIN_ID = 5042002


def is_valid_address(address):
    return bool(re.fullmatch(r"0x[a-fA-F0-9]{40}", address))


def rpc_call(method, params=None):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params or [],
    }

    request = urllib.request.Request(
        RPC_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "arc-usdc-inspector/0.1",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as error:
        raise RuntimeError(f"RPC connection failed: {error}")

    if "error" in data:
        raise RuntimeError(f"RPC error: {data['error']}")

    return data["result"]


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 src/arc_inspector.py <public-address>")
        sys.exit(1)

    address = sys.argv[1]

    if not is_valid_address(address):
        print("Error: invalid EVM address")
        sys.exit(1)

    try:
        chain_id = int(rpc_call("eth_chainId"), 16)
        latest_block = int(rpc_call("eth_blockNumber"), 16)

        raw_balance = int(
            rpc_call("eth_getBalance", [address, "latest"]),
            16,
        )

        native_usdc = raw_balance / 10**18

    except RuntimeError as error:
        print(error)
        sys.exit(1)

    print()
    print("Arc USDC Inspector")
    print("------------------")
    print(f"Address:      {address}")
    print(f"Chain ID:     {chain_id}")
    print(f"Latest block: {latest_block}")
    print(f"Native USDC:  {native_usdc:,.6f} USDC")

    if chain_id == EXPECTED_CHAIN_ID:
        print("Network:      Arc Testnet ✓")
    else:
        print("Network:      Unexpected network")


if __name__ == "__main__":
    main()