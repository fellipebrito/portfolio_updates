import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas_datareader.data as web
import datetime
import os

smart = ['SHV', 'NEAR']
general = ['VTI', 'VTV', 'VOE', 'VBR', 'VEA', 'VWO', 'VTIP', 'AGG', 'MUB', 'BNDX']

today = datetime.date.today()
yesterday = today - datetime.timedelta(days = 1)

def percentage(part, whole):
    return 100 * float(part)/float(whole)

def daily_difference(stock):
    return percentage(stock.iat[1, stock.columns.get_loc('Adj Close')],
                      stock.iat[0, stock.columns.get_loc('Adj Close')]) - 100

def portfolio_daily_diff(portfolio):
    diff = 0
    for fund in portfolio:
        print("Reading " + fund)
        sheet = web.DataReader(fund, 'yahoo', yesterday, today)

        current_diff = daily_difference(sheet)
        print(current_diff)

        diff = diff + daily_difference(sheet)

    return diff

def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}" sound name "Pop"'
              """.format(text, title))

smart_diff_today = round(portfolio_daily_diff(smart), 2)
if (smart_diff_today < 0):
    notify('Portfolio Update', "Today Diff: %s" % smart_diff_today)

general_diff_today = round(portfolio_daily_diff(general), 2)
if (general_diff_today < 0.5 or general_diff_today > 0.2):
    notify('Portfolio Update', "Today Diff: %s" % general_diff_today)
