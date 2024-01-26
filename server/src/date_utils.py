import datetime

def get_today():
    return datetime.date.today(), datetime.date.today()

def get_yesterday():
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    return yesterday, yesterday

def get_last_5_days():
    return datetime.date.today() - datetime.timedelta(days=5), datetime.date.today()

def get_last_month():
    return datetime.date.today() - datetime.timedelta(days=30), datetime.date.today()

def get_last_3_months():
    return datetime.date.today() - datetime.timedelta(days=90), datetime.date.today()

def get_date_range():
    date_range_switcher = {
        '1': get_today,
        '2': get_yesterday,
        '3': get_last_5_days,
        '4': get_last_month,
        '5': get_last_3_months
    }
    user_choice = input("Select date period: [1] (Today) [2] (Yesterday) [3] (Last 5 days) [4] (Last month) [5] (Last 3 months) | (default is 1): ")
    date_range_func = date_range_switcher.get(user_choice, get_today)
    return date_range_func()