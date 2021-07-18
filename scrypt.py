from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from pycbrf.toolbox import ExchangeRates


api_key = "my_api_key"
api_secret = "my_api_secret"

client = Client(api_key, api_secret)

allTickers = client.get_account()["balances"]
portfolio = dict()
rates = ExchangeRates()
RUB = float(rates["USD"].rate)

csv_rows = []
csv_rows.append(", ".join(["Наименование",
                 "Количество",
                 "Цена в BUSD",
                 "Цена в руб.",
                 "Цена в BTC",
                 "Общая стоимоость в BUSD",
                 "Общая стоимоость в руб.",
                 "Общая стоимоость в BTC",
                 "Средняя цена",
                 "Прибыль в BUSD",
                 "Прибыль в %"]))


for ticker in allTickers:
    if float(ticker["free"]) + float(ticker["locked"]):
        portfolio[ticker["asset"]] = float(ticker["free"]) + float(ticker["locked"])


end1 = "Итог:"
end2 = "-"
end3 = "-"
end4 = "-"
end5 = "-"

end6 = 0
end7 = 0
end8 = 0

end9 = 0
end10 = 0
end11 = 0

cost_in_BUSD = 0
sum_in_BUSD = 0
cost_in_RUB = 0
sum_in_RUB = 0
cost_in_BTC = 0
sum_in_BTC = 0
avg_coin_price = 0
profit_in_BUSD = 0
profit_in_perc = 0

for name, count in portfolio.items():
    if name == "USDT" or name == "BUSD":
        continue
    symb = name + "BUSD"
    if symb == "LDBNBBUSD": continue  # Монета, которой нет на биржи но может быть в кошельке
    avg_coin_price = float(client.get_avg_price(symbol=symb)["price"]) * count
    end9 += avg_coin_price

    for coin in client.get_all_tickers():
        if name + "BUSD" == coin["symbol"]:
            cost_in_BUSD = float(coin["price"])
            sum_in_BUSD = count * float(coin["price"])
            end6 += sum_in_BUSD

        if name + "BTC" == coin["symbol"]:
            cost_in_BTC = float(coin["price"])
            sum_in_BTC = count * float(coin["price"])
            end8 += sum_in_BTC

    cost_in_RUB = cost_in_BUSD * RUB
    sum_in_RUB = count * cost_in_BUSD * RUB
    end7 += sum_in_RUB

    profit_in_BUSD = sum_in_BUSD - avg_coin_price
    end10 += profit_in_BUSD
    profit_in_perc = profit_in_BUSD/avg_coin_price * 100
    end11 += profit_in_perc


    csv_rows.append(", ".join([name,
                               str(count),
                               str(cost_in_BUSD),
                               str(cost_in_RUB),
                               str(cost_in_BTC),
                               str(sum_in_BUSD),
                               str(sum_in_RUB),
                               str(sum_in_BTC),
                               str(avg_coin_price),
                               str(profit_in_BUSD),
                               str(profit_in_perc) + "%"
                               ]))

csv_rows.append(", ".join([str(end1),
                           str(end2),
                           str(end3),
                           str(end4),
                           str(end5),
                           str(end6),
                           str(end7),
                           str(end8),
                           str(end9),
                           str(end10),
                           str(end11) + "%"]))


with open ('positions.csv', 'w') as f:
    f.write("\n".join(csv_rows))
