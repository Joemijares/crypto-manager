import datetime
import time

import requests

ONE_LTC = 10**8


def fix_send_tx_amount(transaction, our_addresses):
    """Calculate actual balance change for a transaction."""
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


def _get_address_info(address, latest_block=0):
    """Fetch address information from Blockchair API."""
    # Using Blockchair API for Litecoin
    url = f"https://api.blockchair.com/litecoin/dashboards/address/{address}"
    
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to fetch Litecoin data: {e}")

    if "data" not in data or address not in data["data"]:
        raise ValueError(f"No data found for address {address}")

    addr_data = data["data"][address]["address"]
    transactions_data = data["data"][address]["transactions"]

    # Filter transactions by block height if needed
    if latest_block > 0:
        transactions_data = [
            tx for tx in transactions_data if tx.get("block_id", 0) > latest_block
        ]

    return addr_data, transactions_data


def get_account_info(address, latest_block=0):
    """
    Fetch Litecoin account information and transaction history.
    
    Args:
        address (str): Litecoin address to query
        latest_block (int, optional): Only fetch transactions after this block. Defaults to 0.
    
    Returns:
        dict: Account information including balance, transactions, and metadata
        
    Raises:
        ValueError: If address format is invalid or API request fails
        
    Example:
        >>> wallet = get_account_info("LXYYoi6NrKEJJzXK5xzPnPE2z9Mqwk2FsC")
        >>> print(wallet['balance'])
        10.5
    """
    decimals = len(str(ONE_LTC)) - 1
    
    try:
        addr_data, transactions_data = _get_address_info(address, latest_block)
    except Exception as e:
        raise ValueError(f"Error fetching Litecoin account info: {e}")

    # Calculate balance
    balance_raw = addr_data["balance"]
    
    # Parse transactions
    all_transactions = []
    for tx_hash in transactions_data:
        # Fetch individual transaction details
        try:
            tx_url = f"https://api.blockchair.com/litecoin/dashboards/transaction/{tx_hash}"
            tx_response = requests.get(tx_url, timeout=60)
            tx_response.raise_for_status()
            tx_data = tx_response.json()
            
            if "data" not in tx_data or tx_hash not in tx_data["data"]:
                continue
                
            tx_info = tx_data["data"][tx_hash]["transaction"]
            
            # Determine transaction type and value
            is_sent = False
            tx_value = 0
            
            for inp in tx_data["data"][tx_hash].get("inputs", []):
                if inp.get("recipient") == address:
                    is_sent = True
                    tx_value += inp.get("value", 0)
            
            for outp in tx_data["data"][tx_hash].get("outputs", []):
                if outp.get("recipient") == address:
                    if not is_sent:
                        tx_value += outp.get("value", 0)
            
            transaction = {
                "hash": tx_hash,
                "block_number": tx_info.get("block_id", 0),
                "from": [],
                "to": [],
                "type": "sent" if is_sent else "received",
                "value": round(abs(tx_value) / ONE_LTC, decimals),
                "value_raw": str(abs(tx_value)),
                "fee": round(tx_info.get("fee", 0) / ONE_LTC, decimals),
                "fee_raw": str(tx_info.get("fee", 0)),
                "total": round((abs(tx_value) + tx_info.get("fee", 0)) / ONE_LTC, decimals),
                "total_raw": str(abs(tx_value) + tx_info.get("fee", 0)),
                "dt": datetime.datetime.utcfromtimestamp(
                    tx_info.get("time", time.time())
                ),
                "ts": float(tx_info.get("time", time.time())),
                "confirmed": tx_info.get("block_id", 0) > 0,
            }
            
            all_transactions.append(transaction)
            
        except Exception as e:
            # Skip problematic transactions
            continue

    # Calculate totals
    total_sent = sum(tx["value"] for tx in all_transactions if tx["type"] == "sent")
    total_received = sum(
        tx["value"] for tx in all_transactions if tx["type"] == "received"
    )
    total_sent_raw = sum(
        int(tx["value_raw"]) for tx in all_transactions if tx["type"] == "sent"
    )
    total_received_raw = sum(
        int(tx["value_raw"]) for tx in all_transactions if tx["type"] == "received"
    )

    report = {
        "currency": "LTC",
        "unit": ONE_LTC,
        "address": address,
        "balance": round(balance_raw / ONE_LTC, decimals),
        "balance_raw": str(balance_raw),
        "total_sent": round(total_sent, decimals),
        "total_sent_raw": str(total_sent_raw),
        "total_received": round(total_received, decimals),
        "total_received_raw": str(total_received_raw),
        "transactions": sorted(
            all_transactions, key=lambda x: x["ts"], reverse=True
        ),
        "latest_block_per_address": {
            address: max([tx["block_number"] for tx in all_transactions])
            if all_transactions
            else 0
        },
    }

    return report


if __name__ == "__main__":
    # Example Litecoin address for testing
    # Note: Use a real address with transactions for testing
    try:
        wallet = get_account_info("LTC address here")
        print(f"Balance: {wallet['balance']} LTC")
        print(f"Transactions: {len(wallet['transactions'])}")
        
        for tx in wallet['transactions'][:5]:
            print(
                f"{tx['dt']} {'+' if tx['type'] == 'received' else '-'} "
                f"{tx['value']:.8f} LTC ({tx['hash'][:16]}...)"
            )
    except Exception as e:
        print(f"Example requires a valid Litecoin address: {e}")
