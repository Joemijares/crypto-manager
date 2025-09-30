import datetime
import time

import requests

ONE_DOGE = 10**8


def _get_address_info(address, latest_block=0):
    """Fetch address information from Blockchair API."""
    # Using Blockchair API for Dogecoin
    url = f"https://api.blockchair.com/dogecoin/dashboards/address/{address}"
    
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to fetch Dogecoin data: {e}")

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
    Fetch Dogecoin account information and transaction history.
    
    Args:
        address (str): Dogecoin address to query
        latest_block (int, optional): Only fetch transactions after this block. Defaults to 0.
    
    Returns:
        dict: Account information including balance, transactions, and metadata
        
    Raises:
        ValueError: If address format is invalid or API request fails
        
    Example:
        >>> wallet = get_account_info("DH5yaieqoZN36fDVciNyRueRGvGLR3mr7L")
        >>> print(wallet['balance'])
        1000.0
    """
    decimals = len(str(ONE_DOGE)) - 1
    
    try:
        addr_data, transactions_data = _get_address_info(address, latest_block)
    except Exception as e:
        raise ValueError(f"Error fetching Dogecoin account info: {e}")

    # Calculate balance
    balance_raw = addr_data["balance"]
    
    # Parse transactions
    all_transactions = []
    for tx_hash in transactions_data:
        # Fetch individual transaction details
        try:
            tx_url = f"https://api.blockchair.com/dogecoin/dashboards/transaction/{tx_hash}"
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
                "value": round(abs(tx_value) / ONE_DOGE, decimals),
                "value_raw": str(abs(tx_value)),
                "fee": round(tx_info.get("fee", 0) / ONE_DOGE, decimals),
                "fee_raw": str(tx_info.get("fee", 0)),
                "total": round((abs(tx_value) + tx_info.get("fee", 0)) / ONE_DOGE, decimals),
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
        "currency": "DOGE",
        "unit": ONE_DOGE,
        "address": address,
        "balance": round(balance_raw / ONE_DOGE, decimals),
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
    # Example Dogecoin address for testing
    # Note: Use a real address with transactions for testing
    try:
        wallet = get_account_info("DOGE address here")
        print(f"Balance: {wallet['balance']} DOGE")
        print(f"Transactions: {len(wallet['transactions'])}")
        
        for tx in wallet['transactions'][:5]:
            print(
                f"{tx['dt']} {'+' if tx['type'] == 'received' else '-'} "
                f"{tx['value']:.8f} DOGE ({tx['hash'][:16]}...)"
            )
    except Exception as e:
        print(f"Example requires a valid Dogecoin address: {e}")
        print("Much wow! To the moon! 🚀🐕")
