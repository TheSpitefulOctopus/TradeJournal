from flask import Flask, render_template, request, redirect, session, url_for
from functools import wraps
import pendulum
import calendargen
import os
import db
import chart
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
dbfile = 'db/tradehistory.db'


def user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in session:
            navupdate = db.navupdate()
            print(navupdate)
            numot = navupdate['numofTrades'][0]
            session['today'] = navupdate['today']
            session['tradesthismonth'] = navupdate['tradesthismonth'][0]
            session['tradestoday'] = navupdate['tradestoday'][0]
            session['numberOfTrades'] = numot
            # return True
        else:
            # return False
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@app.route('/calendar')
@app.route('/<int:year>-<int:month>', methods=['GET','POST'])
@user
def index(year=None, month=None):
    # if user():
    db.updateBalance()
    cgen = calendargen.calendarGen(year, month)
    monthName = cgen["monthName"]
    year = cgen['year']
    pm = cgen['pm']
    nm = cgen['nm']
    py = cgen['py']
    ny = cgen['ny']
    monthRange = cgen['monthRange']
    if month == None:
        dt = pendulum.now()
        month = dt.month
        # print(month)
    else:
        month = month
    allTrades = db.monthlyTrades(year,month)
    dayprofits = db.dayprofits(year, month)
    return render_template('index.html', monthName=monthName, year=year, pm=pm, nm=nm,py=py,ny=ny,monthRange=monthRange, month=month, allTrades=allTrades, dayprofits=dayprofits)
    # else:
    #     return redirect('login')


@app.route('/add_trade', methods=['GET', 'POST'])
@user
def add_trade():
    db.navupdate()
    dt = pendulum.now()
    today = dt.to_date_string()
    entryTime = dt.to_time_string()
    exitTime = entryTime
    systems = db.getSystems()
    return render_template("add_trade.html", today=today, entryTime=entryTime, exitTime=exitTime, systems=systems)
    


@app.route('/submit_trade', methods=['POST'])
@user
def submit_trade():
    if request.method=="POST":
        systemsig = []
        ticker = request.form['tickerName'].upper()
        entrydate = request.form["entryDate"]
        exitdate = request.form['exitDate']
        entrytime = request.form['entryTime'] 
        exittime = request.form['exitTime']
        numOfShares = int(request.form["numberOfShares"])
        entryprice = float(request.form['entryPrice'])
        exitprice = float(request.form['exitPrice'])
        commission = request.form["commissions"]
        for item in request.form:
            if 'system_' in item:
                systemsig.append(request.form[item])
        systemsig = ', '.join(systemsig)
        print(systemsig)
        direction = request.form["direction"]

        entrytime_split = entrytime.split(":")
        exittime_split = exittime.split(":")
        dtentry = pendulum.create(2018,1,1,int(entrytime_split[0]),int(entrytime_split[1]),int(entrytime_split[2]))
        dtexit = pendulum.create(2018,1,1,int(exittime_split[0]),int(exittime_split[1]),int(exittime_split[2]))
        tradeDur = str(dtentry.diff(dtexit))
        
        profit = (float(exitprice) - float(entryprice)) * int(numOfShares)
        profit = float("{0:.2f}".format(profit))


        db.addTrade(entrydate,exitdate,entrytime,exittime,tradeDur,numOfShares,direction,entryprice,exitprice,profit,ticker,systemsig)
        db.navupdate()
    return redirect('add_trade')
    

@app.route('/stats', methods=['GET', 'POST'])
# @user
def stats():
    # alltrades = db.getAllTrades()
    alltradesChart = chart.allTradesChart()
    winlosspie = chart.winlossPieChart()
    systempie = chart.systemPieChart()
    statsData = db.statsData()
    profitable = statsData['Profitable']
    loss = statsData['Loss']
    be = statsData['BreakEven']
    averageprofitperday = statsData['averageprofitperday']
    averageprofitpermonth = statsData['averageprofitpermonth']
    averageprofitperquarter = statsData['averageprofitperquarter']
    averageprofitperyear = statsData['averageprofitperyear']
    longestwin = statsData["longestwin"]
    longestwinticker = statsData["longestwinTicker"]
    quickestwin = statsData["quickestwin"]
    quickestwinticker = statsData["quickestwinTicker"]
    longestloss = statsData["longestloss"]
    longestlossticker = statsData["longestlossTicker"]
    quickestloss = statsData["quickestloss"]
    quickestlossticker = statsData["quickestlossTicker"]
    largestprofit = statsData["largestprofit"]
    largestprofitticker = statsData["largestprofitTicker"]
    largestloss = statsData["largestloss"]
    largetslossticker = statsData["largestlossTicker"]
    systemAndCount = statsData['systemAndCount']
    totalNumTrades = statsData['totalNumTrades']
    maxwinsinarow= statsData["maxwinsinarow"]
    maxlossinarow= statsData["maxlossinarow"]

    year = pendulum.today().year
    month = pendulum.today().month
    monthTrades = db.monthlyChartTrades(year, month)
    monthlyChart = chart.monthlyChart(monthTrades)

    weeklyTrades = chart.weeklyChart()
    return render_template('stats.html', alltradeschart=alltradesChart, winlosspie=winlosspie, systempie=systempie, profitable=profitable, loss=loss, be=be, averageprofitperday=averageprofitperday, averageprofitpermonth=averageprofitpermonth, averageprofitperquarter=averageprofitperquarter, averageprofitperyear=averageprofitperyear, longestwin=longestwin, longestwinticker=longestwinticker, quickestwin=quickestwin, quickestwinticker=quickestwinticker, longestloss=longestloss, longestlossticker=longestlossticker, quickestloss=quickestloss, quickestlossticker=quickestlossticker, largestprofit=largestprofit, largestprofitticker=largestprofitticker, largestloss=largestloss, largetslossticker=largetslossticker, systemAndCount=systemAndCount, totalNumTrades=totalNumTrades, maxwinsinarow=maxwinsinarow, maxlossinarow=maxlossinarow, monthlyChart=monthlyChart, weeklyTrades=weeklyTrades)
    

@app.route('/setBalance', methods=['POST'])
@user
def setBalance():
    if request.method == "POST":
        balance = request.form['setBalance']
        db.setStartingBalance(balance)
    return redirect(request.referrer)


@app.route('/<int:year>-<int:month>-<int:day>', methods=['GET', 'POST'])
@user
def dayResults(year=None, month=None, day=None):
    date = {"year":year,"month":month,"day":day}
    dayTrades = db.dayTrades(year, month, day)
    daychart = chart.chartDayTrades(dayTrades)
    dt = pendulum.datetime(year, month, day)
    thedateis = dt.strftime('%A %B %d %Y')
    total = 0.00
    for trade in dayTrades:
        total += float(trade[10])
    totalpl = total
    return render_template("dayResults.html", date=date, dayTrades=dayTrades, daychart=daychart, thedateis=thedateis, totalpl=totalpl)

@app.route('/login', methods=['GET', 'POST'])
def login(username=None, password=None):
    if request.method == "POST":
        username = request.form['username']
        password =  request.form['password']
        user = db.login(username, password)
        
        if user != None:
            session['userid'] = user['userid']
            session['username'] = user['username']
            return redirect('/')
    return render_template('login.html')

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        result = db.register(email,username,password)
        if int(result) > 0:
            message = "You have successfully registered."
            return redirect('login')
        else:
            message = "The email you entered is already in use."
            return redirect('sign_up')
    return render_template('sign_up.html')

@app.route('/logout', methods=['GET', 'POST'])
@user
def logout():
    session.pop('userid')
    session.pop('username')
    return redirect('login')


@app.route('/ptm', methods=['GET'])
@app.route('/ptm-<int:year>-<int:month>', methods=['GET', "POST"])
@user
def ptm(year=None, month=None):
    if year == None or month == None:
        year = pendulum.today().year
        month = pendulum.today().month
    date = {"year": year, "month": month}
    dt = pendulum.datetime(year, month, 1, 1, 1, 1)
    thisMonth = dt.strftime('%B %Y')
    monthTrades = db.monthlyChartTrades(year, month)
    monthlyChart = chart.monthlyChart(monthTrades)
    return render_template('ptm.html', date=date, monthlytrades=monthTrades, monthlychart=monthlyChart, thisMonth=thisMonth)


@app.route('/editdb', methods=['GET', 'POST'])
@user
def editdb():
    db.navupdate()
    alltrades = db.getAllTrades()
    return render_template("editdb.html", alltrades=alltrades)

@app.route('/removeFromDb', methods=['POST'])
@user
def removeFromDb():
    _id = request.form['id']
    db.deleteTrade(_id)
    return 'Successfully removed item with id '+_id

@app.route('/editSystems', methods=["GET", "POST"])
@user
def editSystems():
    if request.method == "POST":
        systemName = request.form['SystemName']
        db.addSystems(systemName)
        return redirect(url_for('editSystems'))
    systemList = db.getSystems()
    return render_template("editSystems.html", systemsList=systemList)

@app.route('/removeSystem', methods=["POST"])
@user
def removeSystem():
    _id = request.form['systemID']
    db.removeSystem(_id)
    return "Successfully Removed System with id " + _id

if __name__ == '__main__':
    db.__init__()
    app.run(host='127.0.0.1', port=8000, debug=True)
