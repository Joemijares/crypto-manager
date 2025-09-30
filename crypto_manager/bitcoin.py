import datetime
import time

import requests

ONE_BTC = 100000000


def proxy_url_for(proxy_params):
    host = proxy_params["host"]
    port = proxy_params.get("port")
    user = proxy_params.get("username")
    password = proxy_params.get("password")

    result = host
    if port:
        result = f"{result}:{port}"

    if user:
        if password:
            result = f"{user}:{password}@{result}"
        else:
            result = f"{user}@{result}"

    if proxy_params["type"] == "socks5":
        return f"socks5://{result}"
    elif proxy_params["type"] == "http":
        return f"http://{result}"

    raise ValueError("unknown proxy type: %s" % proxy_params["type"])


def fix_send_tx_amount(transaction, our_addresses):
    actual_value = 0

    for t_in in transaction["vin"]:
        if t_in["prevout"]["scriptpubkey_address"] in our_addresses:
            actual_value -= t_in["prevout"]["value"]
        else:
            actual_value += t_in["prevout"]["value"]

    is_send = actual_value < 0

    for t_out in transaction["vout"]:
        if not t_out.get("scriptpubkey_address"):
            continue

        if is_send:
            if t_out["scriptpubkey_address"] in our_addresses:
                actual_value += t_out["value"]
        else:
            if t_out["scriptpubkey_address"] not in our_addresses:
                actual_value -= t_out["value"]

    transaction["balance_diff"] = actual_value
    return transaction


def _get_address_info(address, latest_block=0, proxy_info=None):
    if proxy_info:
        proxies = {
            "http": proxy_url_for(proxy_info),
            "https": proxy_url_for(proxy_info),
        }
    else:
        proxies = None

    wallet = requests.get(
        f"https://blockstream.info/api/address/{address}", timeout=60, proxies=proxies
    ).json()

    all_transactions = []
    n_transactions = (
        wallet["chain_stats"]["tx_count"] + wallet["mempool_stats"]["tx_count"]
    )
    last_seen_tx_id = None

    while len(all_transactions) < n_transactions:
        if last_seen_tx_id:
            res = requests.get(
                f"https://blockstream.info/api/address/{address}/txs/chain/{last_seen_tx_id}",
                timeout=60,
                proxies=proxies,
            ).json()
        else:
            res = requests.get(
                f"https://blockstream.info/api/address/{address}/txs",
                timeout=60,
                proxies=proxies,
            ).json()

        for tx in res:
            last_seen_tx_id = tx["txid"]
            fix_send_tx_amount(tx, [address])
            all_transactions.append(tx)

            if (
                tx["status"]["confirmed"]
                and tx["status"]["block_height"] < latest_block
            ):
                return (
                    wallet["chain_stats"],
                    all_transactions,
                    max(
                        [
                            _tx["status"]["block_height"]
                            for _tx in all_transactions
                            if _tx["status"]["confirmed"]
                        ],
                        default=0,
                    ),
                )

    return (
        wallet["chain_stats"],
        all_transactions,
        max(
            [
                _tx["status"]["block_height"]
                for _tx in all_transactions
                if _tx["status"]["confirmed"]
            ],
            default=0,
        ),
    )


def get_account_info(
    address,
    known_addresses=None,
    latest_block_per_address=None,
    skip_linked_addresses=False,
    proxy_info=None,
):
    if not known_addresses:
        known_addresses = []

    if not latest_block_per_address:
        latest_block_per_address = {}

    wallet, all_transactions, latest_block = _get_address_info(
        address, latest_block_per_address.get(address, 0), proxy_info
    )
    latest_block_per_address[address] = latest_block

    for tx in all_transactions:
        if tx["balance_diff"] > 0:
            continue

        for t_in in tx["vin"]:
            if t_in["prevout"]["scriptpubkey_address"] == address:
                continue

            known_addresses.append(t_in["prevout"]["scriptpubkey_address"])

    known_addresses = set(known_addresses)

    if not skip_linked_addresses:
        for known_address in list(known_addresses):
            if known_address == address:
                continue

            our_wallet, our_transactions, latest_block = _get_address_info(
                known_address,
                latest_block_per_address.get(known_address, 0),
                proxy_info,
            )
            latest_block_per_address[known_address] = latest_block

            wallet["spent_txo_sum"] += our_wallet["spent_txo_sum"]
            wallet["funded_txo_sum"] += our_wallet["funded_txo_sum"]

            for tx in our_transactions:
                all_transactions.append(tx)

    known_addresses.add(address)
    all_transactions = [
        fix_send_tx_amount(tx, known_addresses) for tx in all_transactions
    ]

    unique_tx_ids = set()
    unique_transactions = []

    for tx in all_transactions:
        if tx["txid"] in unique_tx_ids:
            continue

        unique_tx_ids.add(tx["txid"])
        unique_transactions.append(tx)

    decimals = len(str(ONE_BTC)) - 1
    now = time.time()

    report = {
        "currency": "BTC",
        "unit": ONE_BTC,
        "address": address,
        "known_addresses": list(known_addresses),
        "latest_block_per_address": latest_block_per_address,
        "total_sent": round(wallet["spent_txo_sum"] / ONE_BTC, decimals),
        "total_received": round(wallet["funded_txo_sum"] / ONE_BTC, decimals),
        "balance": round(
            (wallet["funded_txo_sum"] - wallet["spent_txo_sum"]) / ONE_BTC, decimals
        ),
        "total_sent_raw": str(wallet["spent_txo_sum"]),
        "total_received_raw": str(wallet["funded_txo_sum"]),
        "balance_raw": str(wallet["funded_txo_sum"] - wallet["spent_txo_sum"]),
        "transactions": [
            {
                "hash": transaction["txid"],
                "from": [
                    {
                        "address": t_in["prevout"]["scriptpubkey_address"],
                        "value": round(t_in["prevout"]["value"] / ONE_BTC, decimals),
                        "value_raw": str(t_in["prevout"]["value"]),
                    }
                    for t_in in transaction["vin"]
                ],
                "to": [
                    {
                        "address": t_out["scriptpubkey_address"],
                        "value": round(t_out["value"] / ONE_BTC, decimals),
                        "value_raw": str(t_out["value"]),
                    }
                    for t_out in transaction["vout"]
                    if t_out.get("scriptpubkey_address")
                ],
                "type": "sent" if transaction["balance_diff"] < 0 else "received",
                "fee": round(transaction["fee"] / ONE_BTC, decimals),
                "fee_raw": str(transaction["fee"]),
                "value": round(
                    abs(float(abs(transaction["balance_diff"]) - transaction["fee"]))
                    / ONE_BTC,
                    decimals,
                ),
                "value_raw": str(
                    abs(abs(transaction["balance_diff"]) - transaction["fee"])
                ),
                "total": round(
                    abs(float(transaction["balance_diff"])) / ONE_BTC, decimals
                ),
                "total_raw": str(abs(transaction["balance_diff"])),
                "ts": transaction["status"]["block_time"]
                if transaction["status"]["confirmed"]
                else now,
                "known_change_address": (
                    len(transaction["vout"]) == 1
                    or any(
                        [
                            t_out["scriptpubkey_address"] in known_addresses
                            for t_out in transaction["vout"]
                            if t_out.get("scriptpubkey_address")
                        ]
                    )
                )
                if transaction["balance_diff"] < 0
                else False,
                "dt": datetime.datetime.utcfromtimestamp(
                    transaction["status"]["block_time"]
                )
                if transaction["status"]["confirmed"]
                else datetime.datetime.utcfromtimestamp(now),
                "confirmed": transaction["status"]["confirmed"],
            }
            for transaction in unique_transactions
        ],
    }

    return report


if __name__ == "__main__":
    acc_info = get_account_info(
        "bc1qwrvfsrn2mt0srfkc7petwxfer70y533sac6y2e",
        known_addresses=[
            "bc1qwrvfsrn2mt0srfkc7petwxfer70y533sac6y2e",
        ],
    )

    for tx in sorted(acc_info["transactions"], key=lambda tx: tx["ts"], reverse=True):
        print(
            f"{tx['dt']} {'+' if tx['type'] == 'received' else '-'} {tx['total']:.8f} (no fee={tx['value']:.8f}) {tx['hash']}"
        )
