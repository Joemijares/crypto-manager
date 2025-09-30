import datetime

import requests

from crypto_manager import config

API_BASE = "https://api.etherscan.io/v2/api?chainid=1"
# API_BASE = 'https://api-ropsten.etherscan.io'

ONE_ETHER = 1000000000000000000

CONTRACT_ADDRESS_USDT = "0xdac17f958d2ee523a2206206994597c13d831ec7"
CONTRACT_ADDRESS_BUSD = "0x4fabb145d64652a948d72533023f6e7a623c7c53"
CONTRACT_ADDRESS_USDC = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"

ONE_USDT = 1000000
ONE_BUSD = 1000000000000000000
ONE_USDC = 1000000


def etherscan_request(params):
    raw_resp = requests.get(
        API_BASE,
        params={
            **params,
            "apikey": config.ETHERSCAN_API_KEY,
        },
        headers={
            # need this to prevent CloudFlare blocking it
            "User-Agent": "PostmanRuntime/7.17.1",
        },
        timeout=60,
    )

    try:
        resp = raw_resp.json()
    except ValueError:
        raise ValueError("Got non-json response: %s" % (raw_resp.content,))

    if resp.get("status") != "1":
        raise ValueError("Get balance failed: %s" % (resp,))

    return resp["result"]


def get_raw_ETH_balance(address):
    return int(
        etherscan_request(
            {
                "module": "account",
                "action": "balance",
                "address": address,
                "tag": "latest",
            }
        )
    )


def get_raw_token_balance(address, contract_address):
    return int(
        etherscan_request(
            {
                "module": "account",
                "action": "tokenbalance",
                "contractaddress": contract_address,
                "address": address,
                "tag": "latest",
            }
        )
    )


def get_ETH_balance(address):
    return get_raw_ETH_balance(address)


def latest_eth_transactions(address, internal=False, latest_block=0):
    try:
        txs = etherscan_request(
            {
                "module": "account",
                "action": "txlistinternal" if internal else "txlist",
                "address": address,
                "page": 0,
                "offset": 10000,
                "startblock": latest_block,
                "sort": "desc",
            }
        )
    except ValueError as e:
        print(e)
        if "No transactions found" in str(e):
            # no tx yet, so it's empty
            return []

        raise

    return txs


def latest_erc20_transactions(address, contract_address=None, latest_block=0):
    req = {
        "module": "account",
        "action": "tokentx",
        "address": address,
        "page": 0,
        "offset": 10000,
        "startblock": latest_block,
        "sort": "desc",
    }
    if contract_address:
        req["contractaddress"] = contract_address

    try:
        return etherscan_request(req)
    except ValueError as e:
        print(e)
        if "No transactions found" in str(e):
            # no tx yet, so it's empty
            return []

        raise


def latest_USDT_transactions(address, latest_block=0):
    return latest_erc20_transactions(
        address, contract_address=CONTRACT_ADDRESS_USDT, latest_block=latest_block
    )


def parse_transaction(address, transaction, decimals, one_unit):
    fee = (
        int(transaction["gasUsed"]) * int(transaction["gasPrice"])
        if int(transaction["gasUsed"])
        else 0
    )
    tx_total = (
        abs(int(transaction["value"]) + fee)
        if transaction["from"] == address
        else int(transaction["value"])
    )

    transaction = {
        "hash": transaction["hash"],
        "block_number": transaction["blockNumber"],
        "function_name": transaction.get("functionName"),
        "from": [
            {
                "address": transaction["from"],
                "value": round(int(transaction["value"]) / one_unit, decimals),
                "value_raw": str(transaction["value"]),
            }
        ],
        "to": [
            {
                "address": transaction["to"],
                "value": round(int(transaction["value"]) / one_unit, decimals),
                "value_raw": str(transaction["value"]),
            }
        ],
        "type": "sent" if transaction["from"] == address else "received",
        "value": round(int(transaction["value"]) / one_unit, decimals),
        "value_raw": str(transaction["value"]),
        "fee": round(float(fee) / one_unit, decimals),
        "fee_raw": str(fee),
        "total": round(float(tx_total) / one_unit, decimals),
        "total_raw": str(tx_total),
        "dt": datetime.datetime.utcfromtimestamp(float(transaction["timeStamp"])),
        "ts": float(transaction["timeStamp"]),
        "confirmed": int(transaction["confirmations"]) > 0
        if "confirmations" in transaction
        else True,
    }

    return transaction


def parse_token_transaction(address, transaction, decimals, one_unit):
    transaction = parse_transaction(address, transaction, decimals, one_unit)

    transaction["fee"] = 0
    transaction["fee_raw"] = "0"
    transaction["total"] = round(int(transaction["value_raw"]) / one_unit, decimals)
    transaction["total_raw"] = str(transaction["value_raw"])

    return transaction


def get_account_info_eth(address, latest_block=0):
    decimals = len(str(ONE_ETHER)) - 1
    address = address.lower()
    balance_raw = get_ETH_balance(address)
    eth_report = {
        "currency": "ETH",
        "unit": ONE_ETHER,
        "address": address,
        "total_sent": 0,
        "total_received": 0,
        "balance": round(balance_raw / ONE_ETHER, decimals),
        "total_sent_raw": 0,
        "total_received_raw": 0,
        "balance_raw": str(balance_raw),
        "transactions": [],
    }

    all_hashes = set()

    for transaction in latest_eth_transactions(address, latest_block=latest_block):
        if transaction["hash"] in all_hashes:
            continue

        all_hashes.add(transaction["hash"])

        eth_report["transactions"].append(
            parse_transaction(address, transaction, decimals, ONE_ETHER)
        )

    for transaction in latest_eth_transactions(
        address, internal=True, latest_block=latest_block
    ):
        transaction["hash"] = transaction["hash"] + "-internal"

        if transaction["hash"] in all_hashes:
            continue

        all_hashes.add(transaction["hash"])

        eth_report["transactions"].append(
            parse_transaction(address, transaction, decimals, ONE_ETHER)
        )

    for transaction in eth_report["transactions"]:
        if transaction["type"] == "sent":
            eth_report["total_sent"] += transaction["value"]
            eth_report["total_sent_raw"] += int(transaction["value_raw"])
        else:
            eth_report["total_received"] += transaction["value"]
            eth_report["total_received_raw"] += int(transaction["value_raw"])

    eth_report["total_sent"] = round(eth_report["total_sent"], decimals)
    eth_report["total_received"] = round(eth_report["total_received"], decimals)
    eth_report["total_sent_raw"] = str(eth_report["total_sent_raw"])
    eth_report["total_received_raw"] = str(eth_report["total_received_raw"])
    eth_report["latest_block_per_address"] = {
        address: max([int(t["block_number"]) for t in eth_report["transactions"]])
        if eth_report["transactions"]
        else 0
    }

    return eth_report


def get_account_info_token(
    address, currency, contract_address, one_unit, latest_block=0
):
    decimals = len(str(one_unit)) - 1
    address = address.lower()
    balance_raw = get_raw_token_balance(address, contract_address)
    token_report = {
        "currency": currency,
        "unit": one_unit,
        "address": address,
        "total_sent": 0,
        "total_received": 0,
        "balance": round(balance_raw / one_unit, decimals),
        "total_sent_raw": 0,
        "total_received_raw": 0,
        "balance_raw": str(balance_raw),
        "transactions": [],
    }

    for transaction in latest_erc20_transactions(
        address, contract_address=contract_address, latest_block=latest_block
    ):
        token_report["transactions"].append(
            parse_token_transaction(address, transaction, decimals, one_unit)
        )

    for transaction in token_report["transactions"]:
        if transaction["type"] == "sent":
            token_report["total_sent"] += transaction["value"]
            token_report["total_sent_raw"] += int(transaction["value_raw"])
        else:
            token_report["total_received"] += transaction["value"]
            token_report["total_received_raw"] += int(transaction["value_raw"])

    token_report["total_sent"] = round(token_report["total_sent"], decimals)
    token_report["total_received"] = round(token_report["total_received"], decimals)
    token_report["total_sent_raw"] = str(token_report["total_sent_raw"])
    token_report["total_received_raw"] = str(token_report["total_received_raw"])
    token_report["latest_block_per_address"] = {
        address: max([int(t["block_number"]) for t in token_report["transactions"]])
        if token_report["transactions"]
        else 0
    }

    return token_report


def get_account_info_usdt(address, latest_block=0):
    return get_account_info_token(
        address, "USDT", CONTRACT_ADDRESS_USDT, ONE_USDT, latest_block=latest_block
    )


def get_account_info_busd(address, latest_block=0):
    return get_account_info_token(
        address, "BUSD", CONTRACT_ADDRESS_BUSD, ONE_BUSD, latest_block=latest_block
    )


def get_account_info_usdc(address, latest_block=0):
    return get_account_info_token(
        address, "USDC", CONTRACT_ADDRESS_USDC, ONE_USDC, latest_block=latest_block
    )


if __name__ == "__main__":
    info = get_account_info_eth("0x8672f9c41325Fc9605c36C5542dF4f56c0490805")
    balance = 0
    for tx in sorted(info["transactions"], key=lambda tx: tx["ts"]):
        balance_before = balance

        if tx["type"] == "received":
            amount = tx["value"]
            balance += tx["value"]
        else:
            amount = tx["value"] + tx["fee"]
            balance -= amount

        print(
            f"{tx['dt']} {'+' if tx['type'] == 'received' else '-'} {amount:.8f} (balance={balance_before:.8f} -> {balance:.8f}) {tx['hash']}"
        )

    print(f"Balance: {balance:.18f}")
    print(len(info["transactions"]))
