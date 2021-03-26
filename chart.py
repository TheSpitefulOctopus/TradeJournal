import c3pyo as c3
from collections import Counter
import db


def chartDayTrades(dayTrades):
    x = range(0, len(dayTrades)+1)
    y = [0]
    totalLoss = [0]
    tl = 0
    for item in dayTrades:
        # print(item[10])
        y.append(item[10])
        tl += item[10]
        totalLoss.append(tl)
    dailyChart = c3.LineChart()
    dailyChart.plot(x, y, color="orange", label="Profits")
    dailyChart.plot(x, totalLoss, label="Total P/L:") 
    dailyChart.bind_to('dailyChart')

    return dailyChart.json()


def monthlyChart(monthTrades):
    x = range(0, len(monthTrades)+1)
    y = [0]
    totalLoss = [0]
    tl = 0
    for item in monthTrades:
        y.append(item[10])
        tl += item[10]
        totalLoss.append(tl)
    monthlyChart = c3.LineChart()
    monthlyChart.plot(x, y, color="orange", label="Profits")
    monthlyChart.plot(x, totalLoss, label="Total P/L:")
    monthlyChart.bind_to('monthlychart')

    return monthlyChart.json()


def allTradesChart():
    alltrades = db.getAllTrades()
    startbal = db.getStartingBalance()
    tradeprofits = [startbal[0][1]]
    x = range(0, len(alltrades)+1)
    y = [0]
    totalLoss = [startbal]
    tl = 0
    newbal = startbal[0][1]
    for trade in alltrades:
        y.append(float(trade[10]))
        tl += trade[10]
        newbal += float(trade[10])
        tradeprofits.append(newbal)
        totalLoss.append(tl)
    allTradesChart = c3.LineChart()
    allTradesChart.plot(x,y, color="orange", label="Profits")
    allTradesChart.plot(x, totalLoss, label="Total P/L")
    allTradesChart.plot(x, tradeprofits, label="Account Balance")
    allTradesChart.bind_to('alltradeschart')
    return allTradesChart.json()

def winlossPieChart():
    alltrades = db.getAllTrades()
    win = 0
    loss = 0
    breakEven = 0
    for trade in alltrades:
        if float(trade[10]) > 0.00:
            win += 1
        elif float(trade[10]) < 0.00:
            loss += 1
        else:
            breakEven += 1
    winlossChart = c3.PieChart()
    winlossChart.plot(win, label="Win", color="green")
    winlossChart.plot(loss, label="Loss", color="red")
    winlossChart.plot(breakEven, label="Break Even", color="grey")
    winlossChart.subchart(show_subchart=True)
    winlossChart.bind_to('winlossPie')
    return winlossChart.json()


def systemPieChart():
    systemTrades = db.getAllTrades()
    tradingSystems = []
    for trade in systemTrades:
        t = trade[12].split(',')
        if len(t) > 1:
            for i in t:
                tradingSystems.append(i.strip())
        else:
            tradingSystems.append(trade[12])
    res = Counter(tradingSystems)
    systemPieChart = c3.PieChart()
    for item in res:
        systemPieChart.plot(res[item], label=item)
    systemPieChart.bind_to("systempie")
    return systemPieChart.json()

def weeklyChart():
    weeklyTrades = db.getWeeklyTrades()
    x = range(0, len(weeklyTrades)+1)
    y = [0]
    totalLoss = [0]
    tl = 0
    for item in weeklyTrades:
        y.append(item[10])
        tl += item[10]
        totalLoss.append(tl)
    weeklyChart = c3.LineChart()
    weeklyChart.plot(x, y, color="orange", label="Profits")
    weeklyChart.plot(x, totalLoss, label="Total P/L:")
    weeklyChart.bind_to('weeklychart')
    return weeklyChart.json()


