import random
import time

import requests

from crypto_manager import bitcoin, doge, dot, ethereum, ltc, sol, tron

BTC_EXCHANGE_URL = "https://openexchangerates.org/api/latest.json?app_id=bcd4a32d1c3542a2b3d2de432c1d960e&base=USD"
ETH_EXCHANGE_URL = (
    "https://min-api.cryptocompare.com/data/v2/histohour?fsym=ETH&tsym=USD&limit=1100"
)
DOT_EXCHANGE_URL = (
    "https://min-api.cryptocompare.com/data/v2/histohour?fsym=DOT&tsym=USD&limit=1100"
)
LTC_EXCHANGE_URL = (
    "https://min-api.cryptocompare.com/data/v2/histohour?fsym=LTC&tsym=USD&limit=1100"
)
SOL_EXCHANGE_URL = (
    "https://min-api.cryptocompare.com/data/v2/histohour?fsym=SOL&tsym=USD&limit=1100"
)
DOGE_EXCHANGE_URL = (
    "https://min-api.cryptocompare.com/data/v2/histohour?fsym=DOGE&tsym=USD&limit=1100"
)


def get_exchange_rate(method: str, proxies=None):
    def get_exchange_rate_btc():
        res = requests.get(BTC_EXCHANGE_URL, timeout=60, proxies=proxies).json()

        usd_to_btc_rate = res["rates"]["BTC"]

        return {
            "method_to_usd": 1 / usd_to_btc_rate,
            "usd_to_method": usd_to_btc_rate,
            "unit": bitcoin.ONE_BTC,
            "exchange_rate_ts": res["timestamp"],
        }

    def get_exchange_rate_eth():
        res = requests.get(ETH_EXCHANGE_URL, timeout=60, proxies=proxies).json()
        res = res["Data"]["Data"][-1]

        eth_to_usd_rate = res["open"]

        return {
            "method_to_usd": eth_to_usd_rate,
            "usd_to_method": 1 / eth_to_usd_rate,
            "unit": ethereum.ONE_ETHER,
            "exchange_rate_ts": res["time"],
        }

    def get_exchange_rate_dot():
        res = requests.get(DOT_EXCHANGE_URL, timeout=60, proxies=proxies).json()
        res = res["Data"]["Data"][-1]

        dot_to_usd_rate = res["open"]

        return {
            "method_to_usd": dot_to_usd_rate,
            "usd_to_method": 1 / dot_to_usd_rate,
            "unit": dot.ONE_DOT,
            "exchange_rate_ts": res["time"],
        }

    def get_exchange_rate_ltc():
        res = requests.get(LTC_EXCHANGE_URL, timeout=60, proxies=proxies).json()
        res = res["Data"]["Data"][-1]

        ltc_to_usd_rate = res["open"]

        return {
            "method_to_usd": ltc_to_usd_rate,
            "usd_to_method": 1 / ltc_to_usd_rate,
            "unit": ltc.ONE_LTC,
            "exchange_rate_ts": res["time"],
        }

    def get_exchange_rate_sol():
        res = requests.get(SOL_EXCHANGE_URL, timeout=60, proxies=proxies).json()
        res = res["Data"]["Data"][-1]

        sol_to_usd_rate = res["open"]

        return {
            "method_to_usd": sol_to_usd_rate,
            "usd_to_method": 1 / sol_to_usd_rate,
            "unit": sol.ONE_SOL,
            "exchange_rate_ts": res["time"],
        }

    def get_exchange_rate_doge():
        res = requests.get(DOGE_EXCHANGE_URL, timeout=60, proxies=proxies).json()
        res = res["Data"]["Data"][-1]

        doge_to_usd_rate = res["open"]

        return {
            "method_to_usd": doge_to_usd_rate,
            "usd_to_method": 1 / doge_to_usd_rate,
            "unit": doge.ONE_DOGE,
            "exchange_rate_ts": res["time"],
        }

    if method in ("USDT", "USDT (ERC-20)"):
        return {
            "method_to_usd": 1,
            "usd_to_method": 1,
            "unit": ethereum.ONE_USDT,
            "exchange_rate_ts": time.time(),
        }

    if method in ("USDC", "USDC (ERC-20)"):
        return {
            "method_to_usd": 1,
            "usd_to_method": 1,
            "unit": ethereum.ONE_USDC,
            "exchange_rate_ts": time.time(),
        }

    if method == "USDT (TRC-20)":
        return {
            "method_to_usd": 1,
            "usd_to_method": 1,
            "unit": tron.ONE_USDT,
            "exchange_rate_ts": time.time(),
        }

    fn_map = {
        "BTC": get_exchange_rate_btc,
        "ETH": get_exchange_rate_eth,
        "DOT": get_exchange_rate_dot,
        "LTC": get_exchange_rate_ltc,
        "SOL": get_exchange_rate_sol,
        "DOGE": get_exchange_rate_doge,
    }

    if method in fn_map:
        # retry up to 3 times if failed
        for i in range(3):
            try:
                return fn_map[method]()
            except Exception as e:
                print(f"Error fetching exchange rate for {method}: {e}")
                time.sleep(random.uniform(1, 3))

    raise RuntimeError(f"Unsuported method {method}")


def get_exchange_rate_history(method: str, start: str, end: str, interval: str = "1h"):
    import yfinance as yf

    rates = []

    for row in (
        yf.Ticker(f"{method}-USD")
        .history(start=start, end=end, interval=interval)
        .iterrows()
    ):
        rates.append(
            {
                "exchange_rate_ts": row[0].timestamp(),
                "method_to_usd": float(row[1]["Open"]),
                "usd_to_method": float(1 / row[1]["Open"]),
            }
        )

    return rates


if __name__ == "__main__":
    get_exchange_rate_history("BTC", "2024-09-12", "2024-09-13")
