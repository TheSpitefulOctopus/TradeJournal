import pendulum
import calendar


# Generate information for the calendar to be created
def calendarGen(year=None, month=None):
    #
    #
    # year working properly now
    #
    #
    py = year
    ny = year
    if month == None or year == None:
        dt = pendulum.now()
        month = dt.month
        monthName = dt.format("MMMM")
        year = dt.year
        py = year
        ny = year
    else:
        dt = pendulum.Pendulum(year, month, 1)
        month = dt.month
        monthName = dt.format("MMMM")
        year = year
    #previous month
    pm = dt.subtract(months=1)
    pm = pm.month
    if pm == 12:
        py = dt.subtract(years=1)
        py = py.year
    #next month
    nm = dt.add(months=1)
    nm = nm.month
    if nm == 1:
        ny = dt.add(years=1)
        ny = ny.year
    # import calendar
    monthRange = []
    c = calendar.TextCalendar(calendar.SUNDAY)
    for i in c.itermonthdays(year, month):
        monthRange.append(i)
    return {
        "monthName": monthName,
        "year": year,
        "pm": pm,
        "nm": nm,
        "py": py,
        "ny": ny,
        "monthRange": monthRange
    }
