import sqlite3
import pendulum
from collections import Counter

dbfile = "db/tradehistory.db"

def __init__():
    # create the database if it dosent exist already
    try:
        conn = sqlite3.connect(dbfile)
        curr = conn.cursor()
        curr.execute("CREATE TABLE IF NOT EXISTS tradehistory (id INTEGER PRIMARY KEY AUTOINCREMENT, entryDate TEXT, exitDate TEXT, entryTime TEXT, exitTime TEXT, tradeDur TEXT, shares INT, tradeDir TEXT, entryPrice REAL, exitPrice REAL, profit REAL, ticker TEXT, systemSig TEXT)")
        curr.execute("CREATE TABLE IF NOT EXISTS startingBalance (id INTEGER PRIMARY KEY UNIQUE, startBalance INT) ")
        curr.execute("INSERT INTO startingBalance VALUES (NULL, 10000)")
        # curr.execute("CREATE TABLE IF NOT EXISTS startingBalance (id INTEGER PRIMARY KEY UNIQUE, startBalance INT)")
        # curr.execute("CREATE TABLE IF NOT EXISTS currentBalance (id INTEGER PRIMARY KEY UNIQUE, currentBalance INT DEFAULT 10000)")
        curr.execute("CREATE TABLE IF NOT EXISTS currentBalance (id INTEGER PRIMARY KEY UNIQUE, currentBalance INT)")
        curr.execute("CREATE TABLE IF NOT EXISTS Systems (id INTEGER PRIMARY KEY UNIQUE, systemName TEXT)")
        conn.commit()
        conn.close()
        print("DB has been created at db/")
    except Exception:
        print("DB already Exists or there was an error")
    return

# add a new trade into the database
def addTrade(entrydate=None, exitdate=None, entrytime=None, exittime=None, tradeDur=None, numOfShares=None, direction=None, entryprice=None, exitprice=None, profit=None, ticker=None, systemsig=None):
    conn = sqlite3.connect(dbfile)
    curr = conn.cursor()
    addedTrade = curr.execute("INSERT INTO tradehistory VALUES(NULL,?,?,?,?,?,?,?,?,?,?,?,?)",(entrydate, exitdate, entrytime, exittime, tradeDur, numOfShares, direction, entryprice, exitprice, profit, ticker, systemsig))
    addedTrade.fetchone()
    conn.commit()
    conn.close()
    updateBalance()
    navupdate()
    return

# get all of the trades made for the month
def monthlyTrades(year=None, month=None):
    year = year
    month = month
    if len(str(month)) < 2:
        month = "0"+str(month)
    date = str(year)+"-"+str(month)+"-%"
    # print(date)
    conn = sqlite3.connect(dbfile)
    curr = conn.cursor()
    query = curr.execute("SELECT entryDate, profit, ticker FROM tradehistory WHERE entryDate LIKE ?",[str(date)])
    # query = curr.execute("SELECT exitDate, profit, ticker FROM tradehistory WHERE entryDate LIKE ?",[str(date)])
    allTrades = query.fetchall()
    conn.close()
    # print(allTrades)
    return allTrades

#get all of the trades for the day
def dayTrades(year=None, month=None, day=None):
    year = year
    month = month
    if len(str(month)) < 2:
        month = "0"+str(month)
    day = day
    if len(str(day)) < 2:
        day = "0"+str(day)
    date = str(year)+"-"+str(month)+"-"+str(day)
    conn = sqlite3.connect(dbfile)
    curr = conn.cursor()
    query = curr.execute("SELECT * FROM tradehistory WHERE exitDate LIKE ?",[str(date)])
    allDayTrades = query.fetchall()
    conn.close()
    return allDayTrades

# get total profit for the day
def dayprofits(year=None, month=None):
    year = year
    month = month
    if len(str(month)) < 2:
        month = "0"+str(month)
    date = str(year)+"-"+str(month)+"-%"
    conn = sqlite3.connect(dbfile)
    curr = conn.cursor()
    query = curr.execute("SELECT entryDate, profit FROM tradehistory WHERE entryDate LIKE ?", [str(date)])
    dayprofits = query.fetchall()
    conn.close()
    
    dayprofits = [(uk, sum([vv for kk, vv in dayprofits if kk == uk])) for uk in set([k for k, v in dayprofits])]
    return dayprofits

# set the balance your account is starting with
def setStartingBalance(balance):
    startingBalance = int(balance.split('.')[0])
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    c.execute("REPLACE INTO startingBalance VALUES(1,?)",[startingBalance])
    conn.commit()
    conn.close()
    updateBalance()
    return

# get the starting balance from the db
def getStartingBalance():
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    res = c.execute("SELECT * FROM startingBalance")
    res = res.fetchall()
    conn.close()
    updateBalance()
    return res

# update the balance in the db
def updateBalance():
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    startbal = c.execute("SELECT startBalance FROM startingBalance")
    try:
        startbal = startbal.fetchall()[0][0]
    except Exception:
        startbal = int(0)    
    allprofit = c.execute("SELECT SUM(profit) from tradehistory")
    allprofit = allprofit.fetchall()[0][0]
    if allprofit == None:
        allprofit = 0.00
    curbal = startbal + allprofit
    c.execute("REPLACE INTO currentBalance VALUES(1,?)",[curbal])
    conn.commit() 
    conn.close()
    return

#keep the navigation bar updated when new trades are added
def navupdate():
    year = str(pendulum.today().year)
    month = str(pendulum.today().month)
    day = str(pendulum.today().day)
    if len(month) < 2:
        month = "0"+str(month)
    if len(day) < 2:
        day = "0"+str(day)
    ttday = year+"-"+month+"-"+day
    thismonth = year+"-"+month+"-%"
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    numot = c.execute("SELECT count(id) FROM tradehistory")
    numot = numot.fetchone()
    tradestoday = c.execute("SELECT count(*) FROM tradehistory WHERE entryDate LIKE ?", [str(ttday)])
    tradestoday = tradestoday.fetchone()
    ttm = c.execute("SELECT count(*) FROM tradehistory WHERE entryDate LIKE ?", [str(thismonth)])
    ttm = ttm.fetchone()
    conn.close()
    todaysDate = str(pendulum.today().year)+ "-"+str(pendulum.today().month)+ "-"+str(pendulum.today().day)
    return {"numofTrades":numot, "today":todaysDate, "tradestoday":tradestoday, "tradesthismonth":ttm}


# get all trades for the month
def monthlyChartTrades(year=None, month=None):
    year = year
    month = month
    if len(str(month)) < 2:
        month = "0"+str(month)
    date = str(year)+"-"+str(month)+"-%"
    conn = sqlite3.connect(dbfile)
    curr = conn.cursor()
    query = curr.execute("SELECT * FROM tradehistory WHERE entryDate LIKE ?", [str(date)])
    allTrades = query.fetchall()
    conn.close()
    return allTrades


# get all trades for the week
def getWeeklyTrades():
    conn = sqlite3.connect(dbfile)
    curr = conn.cursor()
    query = curr.execute("SELECT * FROM tradehistory WHERE exitDate >= DATE('now','weekday 0', '-7 days')")
    weeklyTrades = query.fetchall()
    conn.close()
    return weeklyTrades

# get all of the trades from the db
def getAllTrades():
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    res = c.execute("SELECT * FROM tradehistory")
    getAllTrades = res.fetchall()
    conn.close()
    return getAllTrades


# remove a trade from the db
def deleteTrade(_id):
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    c.execute("DELETE FROM tradehistory WHERE id == ?",[_id])
    conn.commit()
    conn.close()
    return

# add the name of a system to keep track of which ones are generating a profit
def addSystems(systemName):
    # print(systemName)
    conn = sqlite3.connect(dbfile)
    cur = conn.cursor()
    cur.execute("INSERT INTO Systems VALUES (NULL,?)",[systemName])
    conn.commit()
    conn.close()
    return

# get the name of the system used
def getSystems():
    conn = sqlite3.connect(dbfile)
    cur = conn.cursor()
    systems = cur.execute("SELECT * FROM Systems")
    systems = systems.fetchall()
    conn.close()
    return systems

# Remove the system from the database
def removeSystem(_id):
    conn = sqlite3.connect(dbfile)
    cur = conn.cursor()
    cur.execute("DELETE FROM Systems WHERE id == ?",[_id])
    conn.commit()
    conn.close()
    return

#get all of the data needed for the stats page  
#this page is still a wip and will display more information at some point
def statsData():
    statsData = {}
    conn = sqlite3.connect(dbfile)
    cur = conn.cursor()
    trades = cur.execute("SELECT * FROM tradehistory")
    trades = trades.fetchall()
    
    statsData['totalNumTrades'] = len(trades)
    # calculate win vs loss
    win = 0
    loss = 0
    be = 0
    for trade in trades:
        if float(trade[10]) > 0.00:
            win += 1
        elif float(trade[10]) < 0.00:
            loss += 1
        else:
            be += 1
    statsData["Profitable"] = win
    statsData["Loss"] = loss
    statsData["BreakEven"] = be
    # end win vs loss

    # calculate average profit per day
    averageprofitperday = cur.execute("SELECT AVG(profit) FROM tradehistory GROUP BY exitDate")
    averageprofitperday = averageprofitperday.fetchall()
    appd = 0
    for trade in averageprofitperday:
        appd += float(trade[0])
    appd = '{0:0.2f}'.format(appd/len(averageprofitperday))
    statsData['averageprofitperday'] = appd
    # end average profit per day

    # calculate average profit per month
    appm = cur.execute("SELECT AVG(profit) FROM tradehistory GROUP BY strftime('%m', exitDate);")
    appm = appm.fetchall()
    averageprofitpermonth = 0
    for ret in appm:
        averageprofitpermonth += float(ret[0])
    averageprofitpermonth = '{0:0.2f}'.format(averageprofitpermonth/len(appm))
    statsData['averageprofitpermonth'] = averageprofitpermonth
    # end average profit per month

    # calculate average profit per quarter
    appq = cur.execute("SELECT AVG(profit) FROM tradehistory GROUP BY strftime('%m', exitDate)/4;")
    appq = appq.fetchall()
    averageprofitperquarter = 0
    for ret in appm:
        averageprofitperquarter += float(ret[0])
    averageprofitperquarter = '{0:0.2f}'.format(averageprofitperquarter/len(appq))
    statsData['averageprofitperquarter'] = averageprofitperquarter
    # end average profit per month

    # calculate average profit per year
    appy = cur.execute("SELECT sum(profit) FROM tradehistory GROUP BY strftime('%y', exitDate);")
    appy = appy.fetchall()
    averageprofitperyear = 0
    for ret in appm:
        averageprofitperyear += float(ret[0])
    averageprofitperyear = '{0:0.2f}'.format(averageprofitperyear/len(appy))
    statsData['averageprofitperyear'] = averageprofitperyear
    # end average profit per year

    # trades by system
    # systemNames = cur.execute("SELECT systemName from Systems")
    tradingSystems = []
    for trade in trades:
        t = trade[12].split(',')
        if len(t) > 1:
            for i in t:
                tradingSystems.append(i.strip())
        else:
            tradingSystems.append(trade[12])
    res = Counter(tradingSystems)
    # for item in res:
    #     print(item, res[item])
    statsData['systemAndCount'] = res
    # end trades by system

    # win/loss by system
    # sbwin = 0
    # sbloss = 0
    # b70win = 0
    # b70loss = 0
    # b200win = 0
    # b200loss = 0
    # superwin = 0
    # superloss = 0
    # expwin = 0
    # exploss = 0
    # for trades in alltradehistory:
    #     trade = trades[12].split(',')
    #     profit = trades[10]
    #     for t in trade:
    #         t = t.lstrip()
    #         if 'TSO_SuperBreakout' in t and profit > 0:
    #             sbwin += 1
    #         if 'TSO_SuperBreakout' in t and profit < 0:
    #             sbloss += 1

    #         if 'TSO_70Less' in t and profit > 0:
    #             b70win += 1
    #         if 'TSO_70Less' in t and profit < 0:
    #             b70loss += 1

    #         if 'TSO_200Break' in t and profit > 0:
    #             b200win += 1
    #         if 'TSO_200Break' in t and profit < 0:
    #             b200loss += 1

    #         if 'TSO_SuperVolume' in t and profit > 0:
    #             superwin += 1
    #         if 'TSO_SuperVolume' in t and profit < 0:
    #             superloss += 1

    #         if 'TSO_Explosion' in t and profit > 0:
    #             expwin += 1
    #         if 'TSO_Explosion' in t and profit < 0:
    #             exploss += 1
    # end win/loss by system

    # trade duration
    # tradeDuration = []
    # for eachTrade in trade:
    #     tradeDuration.append(eachTrade[5])
    # statsData['tradeDuration'] = tradeDuration
    # end trade duration

    # max wins in a row
    count = 0
    maxcount = 0
    for i in trades:
        if i[10] > 0:
            count += 1
        elif count > maxcount:
            maxcount = count
            count = 0
        else:
            count = 0
    if count > maxcount:
        maxcount = count

    maxwin = maxcount
    statsData["maxwinsinarow"] = maxwin
    # end max wins in a row

    # max loss in a row
    count = 0
    maxcount = 0
    for i in trades:
        if i[10] < 0:
            count += 1
        elif count > maxcount:
            maxcount = count
            count = 0
        else:
            count = 0
    if count > maxcount:
        maxcount = count

    maxloss = maxcount
    statsData["maxlossinarow"] = maxloss
    # end max loss in a row

    # longest and quickest winning trade
    longestwins = cur.execute('SELECT max(tradeDur), ticker FROM tradehistory WHERE tradeDur LIKE "%hour%" AND profit > 0')
    longestwins = longestwins.fetchall()
    if longestwins[0][0] == None:
        longestwins = cur.execute('SELECT max(tradeDur), ticker FROM tradehistory WHERE tradeDur LIKE "%minute%" AND profit > 0')
        longestwins = longestwins.fetchall()
    quickestwins = cur.execute('SELECT min(tradeDur), ticker FROM tradehistory WHERE tradeDur LIKE "%seconds%" AND profit > 0')
    quickestwins = quickestwins.fetchall()
    if quickestwins[0][0] == None:
        quickestwins = cur.execute('SELECT min(tradeDur), ticker FROM tradehistory WHERE profit > 0')
        quickestwins = quickestwins.fetchall()
    longestwin = longestwins[0][0]
    longestwinTicker = longestwins[0][1]
    quickestwin = quickestwins[0][0]
    quickestwinTicker = quickestwins[0][1]
    statsData["longestwin"] = longestwin
    statsData["longestwinTicker"] = longestwinTicker
    statsData["quickestwin"] = quickestwin
    statsData["quickestwinTicker"] = quickestwinTicker
    # end longest and quickest winning trade

    # longest and quickest losing trade
    longestlosss = cur.execute('SELECT max(tradeDur), ticker FROM tradehistory WHERE tradeDur like "%hour%" and profit < 0')
    longestlosss = longestlosss.fetchall()
    if longestlosss[0][0] == None:
        longestloss = cur.execute('SELECT max(tradeDur), ticker FROM tradehistory WHERE tradeDur LIKE "%minute%" AND profit < 0')
        longestloss = longestloss.fetchall()
    quickestlosss = cur.execute('SELECT min(tradeDur), ticker FROM tradehistory WHERE tradeDur LIKE "%seconds%" AND profit < 0')
    quickestlosss = quickestlosss.fetchall()
    if quickestlosss[0][0] == None:
        quickestlosss = cur.execute('SELECT min(tradeDur), ticker FROM tradehistory WHERE profit < 0')
        quickestlosss = quickestlosss.fetchall()
    longestloss = longestlosss[0][0]
    longestlossTicker = longestlosss[0][1]
    quickestloss = quickestlosss[0][0]
    quickestlossTicker = quickestlosss[0][1]
    statsData["longestloss"] = longestloss
    statsData["longestlossTicker"] = longestlossTicker
    statsData["quickestloss"] = quickestloss
    statsData["quickestlossTicker"] = quickestlossTicker
    # end longest and quickest losing trade

    # longest and quickest winning trade
    largestprofits = cur.execute('SELECT max(profit), ticker FROM tradehistory WHERE profit > 0')
    largestprofits = largestprofits.fetchall()
    largestprofit = largestprofits[0][0]
    largestprofitTicker = largestprofits[0][1]
    statsData["largestprofit"] = largestprofit
    statsData["largestprofitTicker"] = largestprofitTicker
    # end longest and quickest winning trade

    # longest and quickest losing trade
    largestlosss = cur.execute('SELECT min(profit), ticker FROM tradehistory WHERE profit < 0')
    largestlosss = largestlosss.fetchall()
    largestloss = largestlosss[0][0]
    largestlossTicker = largestlosss[0][1]
    statsData["largestloss"] = largestloss
    statsData["largestlossTicker"] = largestlossTicker
    # end longest and quickest losing trade

    conn.close()
    return statsData
