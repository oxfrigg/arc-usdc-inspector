import json
import re
import sys
import urllib.error
import urllib.request


RPC_URL = "https://rpc.testnet.arc.network"
EXPECTED_CHAIN_ID = 5042002

USDC_ERC20_ADDRESS = "0x3600000000000000000000000000000000000000"
BALANCE_OF_SELECTOR = "70a08231"


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
            "User-Agent": "arc-usdc-inspector/0.2",
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


def build_balance_of_call(address):
    clean_address = address[2:].lower()
    padded_address = clean_address.rjust(64, "0")

    return "0x" + BALANCE_OF_SELECTOR + padded_address


def get_erc20_usdc_balance(address):
    call_data = build_balance_of_call(address)

    result = rpc_call(
        "eth_call",
        [
            {
                "to": USDC_ERC20_ADDRESS,
                "data": call_data,
            },
            "latest",
        ],
    )

    return int(result, 16)


def format_usdc(raw_micro_usdc):
    whole = raw_micro_usdc // 10**6
    fraction = raw_micro_usdc % 10**6

    return f"{whole:,}.{fraction:06d}"


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

        native_raw = int(
            rpc_call("eth_getBalance", [address, "latest"]),
            16,
        )

        erc20_raw = get_erc20_usdc_balance(address)

    except RuntimeError as error:
        print(error)
        sys.exit(1)

    # Native USDC uses 18-decimal EVM precision.
    # The ERC-20 interface exposes the same underlying balance
    # at standard USDC 6-decimal precision.
    native_as_micro_usdc = native_raw // 10**12

    representations_match = native_as_micro_usdc == erc20_raw

    print()
    print("Arc USDC Inspector")
    print("------------------")
    print(f"Address:          {address}")
    print(f"Chain ID:         {chain_id}")
    print(f"Latest block:     {latest_block}")
    print(f"Native USDC:      {format_usdc(native_as_micro_usdc)} USDC")
    print(f"ERC-20 interface: {format_usdc(erc20_raw)} USDC")

    if representations_match:
        print("Representation:   matched ✓")
    else:
        print("Representation:   mismatch")

    if chain_id == EXPECTED_CHAIN_ID:
        print("Network:          Arc Testnet ✓")
    else:
        print("Network:          Unexpected network")


if __name__ == "__main__":
    main()