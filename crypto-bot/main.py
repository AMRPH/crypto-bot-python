import urllib.request as api
import time

from config import api_key, commission
from operation import Operation

operation = Operation.BUY

walletUSD = 1000
walletBTC = 0.0
costBTC = None
lastCostBTC = None
buyCostBTC = None

buy_dip_threshold = 0.002
buy_upward_threshold = 0.003

sell_loss_threshold = 0.002
sell_profit_threshold = 0.003

listCost = [None, None, None]


def startBot():
    global costBTC

    while True:
        getCostBTC()
        listCost.insert(0, costBTC)

        makeTrade()
        log()

        time.sleep(1800)


def makeTrade():
    global operation, costBTC, lastCostBTC, buyCostBTC, listCost, walletUSD, walletBTC

    if listCost[1] is not None:
        lastCostBTC = listCost[1]

        if operation is Operation.BUY:
            if 1 - costBTC / lastCostBTC >= buy_dip_threshold:
                buyBTC(walletUSD * 0.2)

                buyCostBTC = costBTC
                operation = Operation.SELL

            if costBTC / lastCostBTC - 1 >= buy_upward_threshold:
                buyBTC(walletUSD * 0.25)

                buyCostBTC = costBTC
                operation = Operation.SELL
        else:
            if 1 - costBTC / buyCostBTC >= sell_loss_threshold:
                sellBTC(walletBTC)

                buyCostBTC = None
                operation = Operation.BUY

            if costBTC / lastCostBTC - 1 >= sell_profit_threshold:
                sellBTC(walletBTC)

                buyCostBTC = None
                operation = Operation.BUY


def sellBTC(amountBTC):
    global walletUSD, walletBTC, costBTC
    walletBTC -= amountBTC
    walletUSD += amountBTC * costBTC * (1 - commission)


def buyBTC(amountUSD):
    global walletUSD, walletBTC, costBTC
    walletUSD -= amountUSD
    walletBTC += amountUSD / costBTC * (1 - commission)


def getCostBTC():
    global costBTC
    url = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD&api_key=" + api_key

    costBTC = float(api.urlopen(url).read().decode('utf-8')[7:-1])


def log():
    global operation, costBTC, lastCostBTC, buyCostBTC, walletUSD, walletBTC

    if lastCostBTC is not None:
        if 1 - (costBTC / lastCostBTC) > 0:
            print("BTC -" + str(1 - costBTC / lastCostBTC)[:6] + "%")

        if (costBTC / lastCostBTC) - 1 > 0:
            print("BTC +" + str(costBTC / lastCostBTC - 1)[:6] + "%")

        print("BTC "+ str(costBTC - lastCostBTC)[:4]+"$")

    print("walletUSD: " + str(walletUSD))
    print("walletBTC: " + str(walletBTC))
    print("lastCostBTC: " + str(lastCostBTC))
    print("costBTC: " + str(costBTC))
    print("buyCostBTC: " + str(buyCostBTC))
    print("operation: " + str(operation))
    print(" ")


startBot()
