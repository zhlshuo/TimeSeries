"""
Created on Sun Dec 24 09:00:27 2017

@author: lishuo
"""
import datetime as dt

from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday, nearest_workday, \
    USMartinLutherKingJr, USPresidentsDay, GoodFriday, USMemorialDay, \
    USLaborDay, USThanksgivingDay


class USTradingCalendar(AbstractHolidayCalendar):
    rules = [
        Holiday('NewYearsDay', month=1, day=1, observance=nearest_workday),
        USMartinLutherKingJr,
        USPresidentsDay,
        GoodFriday,
        USMemorialDay,
        Holiday('USIndependenceDay', month=7, day=4, observance=nearest_workday),
        USLaborDay,
        USThanksgivingDay,
        Holiday('Christmas', month=12, day=25, observance=nearest_workday)
    ]

def date_range(start_date, end_date, holcal=USTradingCalendar()):
    holidays = map(lambda x: x.date(), holcal.holidays(start_date, end_date))
    
    dates = []
    for day in range((end_date - start_date).days):
        date = start_date + dt.timedelta(days=day)
        if date.weekday() >= 5 or date in holidays:
            continue
        dates.append(date)
        
    return dates

if __name__ == '__main__':
    dates = date_range(dt.date(2017,1,1), dt.date(2017,12,31))