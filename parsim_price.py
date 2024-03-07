import requests


def get_price_history(cryptocurrency, year):
    prices = []
    for month in range(1, 13):
        url = f"https://api.coinbase.com/v2/prices/{cryptocurrency}-USD/spot?date={year}-{month:02d}-01"
        response = requests.get(url)
        data = response.json()
        price = data['data']['amount']
        prices.append((f"{year}-{month:02d}", price))  # Добавляем дату и цену в список
    return prices


# Пример использования функции
btc_prices = get_price_history("BTC", 2023)
eth_prices = get_price_history("ETH", 2023)
xrp_prices = get_price_history("XRP", 2023)

print(btc_prices)
print(eth_prices)
print(xrp_prices)
