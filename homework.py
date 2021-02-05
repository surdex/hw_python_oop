import datetime as dt


class Calculator:
    def __init__(self, limit: float):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        cnt_expense = 0
        date_today = dt.datetime.now().date()
        for i in range(len(self.records)):
            if self.records[i].date == date_today:
                cnt_expense += self.records[i].amount
        return round(cnt_expense, 2)

    def get_week_stats(self):
        cnt_expense = 0
        date_today = dt.datetime.now().date()
        last_week = date_today - dt.timedelta(days=6)
        for i in range(len(self.records)):
            if last_week <= self.records[i].date <= date_today:
                cnt_expense += self.records[i].amount
        return round(cnt_expense, 2)


class CashCalculator(Calculator):
    USD_RATE = 64.78
    EURO_RATE = 89.51

    def get_today_cash_remained(self, currency):
        cash_remained = self.limit - self.get_today_stats()
        currency_key = {
                         'usd': 'USD',
                         'eur': 'Euro',
                         'rub': 'руб'
                         }
        if currency == 'usd':
            cash_remained /= CashCalculator.USD_RATE
        elif currency == 'eur':
            cash_remained /= CashCalculator.EURO_RATE
        if cash_remained > 0:
            return (f'На сегодня осталось '
                    f'{round(cash_remained, 2)} {currency_key[currency]}')
        elif cash_remained == 0:
            return 'Денег нет, держись'
        else:
            return (f'Денег нет, держись: твой долг - '
                    f'{round(abs(cash_remained), 2)} {currency_key[currency]}')


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        calories_remained = self.limit - self.get_today_stats()
        if calories_remained > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей'
                    f' калорийностью не более {round(calories_remained)} кКал')
        else:
            return 'Хватит есть!'


class Record:
    def __init__(self, amount: float, comment='',
                 date=dt.datetime.now().strftime("%d.%m.%Y")):
        self.amount = amount
        self.comment = comment
        self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
