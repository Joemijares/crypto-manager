import datetime

import requests

API_BASE = "https://api.trongrid.io/v1"

ADDRESS_USDT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
ONE_USDT = 1000000


def get_latest_transactions(address, latest_block_ts=0):
    url = f"https://api.trongrid.io/v1/accounts/{address}/transactions?limit=200&min_timestamp={latest_block_ts}"

    response = requests.get(url, timeout=60).json()
    return response


def get_latest_trc20_transactions(address, latest_block_ts=0):
    url = f"https://api.trongrid.io/v1/accounts/{address}/transactions/trc20?limit=200&min_timestamp={latest_block_ts}"

    response = requests.get(url, timeout=60).json()
    return response


def latest_USDT_transactions(address, latest_block_ts=0):
    all_transactions = get_latest_trc20_transactions(
        address, latest_block_ts=latest_block_ts
    )
    return [
        transaction
        for transaction in all_transactions["data"]
        if transaction["token_info"].get("address") == ADDRESS_USDT
    ]


def get_account_info_usdt(address, latest_block_ts=0):
    url = f"https://apilist.tronscan.org/api/account?address={address}"

    response = requests.get(url, timeout=60).json()

    report = {
        "currency": "USDT (TRC-20)",
        "unit": ONE_USDT,
        "address": address,
        "total_sent": 0,
        "total_received": 0,
        "balance": 0,
        "total_sent_raw": 0,
        "total_received_raw": 0,
        "balance_raw": 0,
        "transactions": [],
    }

    if not response:
        report["balance"] = 0
        return report

    usdt_info = [
        token for token in response["tokens"] if token["tokenId"] == ADDRESS_USDT
    ]

    if not usdt_info:
        report["balance"] = 0
        return report

    decimals = len(str(ONE_USDT)) - 1
    usdt_info = usdt_info[0]
    report["balance"] = round(float(usdt_info["balance"]) / ONE_USDT, decimals)
    report["balance_raw"] = str(usdt_info["balance"])

    transactions = latest_USDT_transactions(address, latest_block_ts=latest_block_ts)

    for transaction in transactions:
        transaction = {
            "hash": transaction["transaction_id"],
            "from": [
                {
                    "address": transaction["from"],
                    "value": round(float(transaction["value"]) / ONE_USDT, decimals),
                    "value_raw": str(transaction["value"]),
                }
            ],
            "to": [
                {
                    "address": transaction["to"],
                    "value": round(float(transaction["value"]) / ONE_USDT, decimals),
                    "value_raw": str(transaction["value"]),
                }
            ],
            "type": "sent" if transaction["from"] == address else "received",
            "value": round(float(transaction["value"]) / ONE_USDT, decimals),
            "value_raw": str(transaction["value"]),
            "fee": 0,
            "fee_raw": str(0),
            "total": round(float(transaction["value"]) / ONE_USDT, decimals),
            "total_raw": str(transaction["value"]),
            "dt": datetime.datetime.utcfromtimestamp(
                float(transaction["block_timestamp"] / 1000)
            ),
            "ts": float(transaction["block_timestamp"]) / 1000,
            "block_ts": transaction["block_timestamp"],
            "confirmed": transaction.get("block_timestamp", 0) > 0,
        }

        report["transactions"].append(transaction)

        if transaction["type"] == "sent":
            report["total_sent"] += transaction["value"]
            report["total_sent_raw"] += int(transaction["value_raw"])
        else:
            report["total_received"] += transaction["value"]
            report["total_received_raw"] += int(transaction["value_raw"])

    report["total_sent"] = round(report["total_sent"], decimals)
    report["total_received"] = round(report["total_received"], decimals)
    report["total_sent_raw"] = str(report["total_sent_raw"])
    report["total_received_raw"] = str(report["total_received_raw"])
    report["latest_block_per_address"] = {
        address: max([t["block_ts"] for t in report["transactions"]])
        if report["transactions"]
        else 0
    }

    return report


if __name__ == "__main__":
    import pprint

    res = get_account_info_usdt("TADCt9L4JjrSrCLM2ZtVcs4yuhWoFTxYbT", latest_block_ts=0)
    pprint.pprint(res)
