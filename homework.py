import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        date_today = dt.date.today()
        return sum(rec_code.amount for rec_code in self.records
                   if rec_code.date == date_today)

    def get_today_remainder(self):
        return (self.limit - self.get_today_stats())

    def get_week_stats(self):
        date_today = dt.date.today()
        last_week = date_today - dt.timedelta(days=6)
        return sum(rec_code.amount for rec_code in self.records
                   if last_week <= rec_code.date <= date_today)


class CashCalculator(Calculator):
    USD_RATE = 64.78
    EURO_RATE = 89.51
    RUB_RATE = 1.00

    def get_today_cash_remained(self, currency):
        cash_remained = self.get_today_remainder()
        if cash_remained == 0:
            return 'Денег нет, держись'
        currency_key = {
            'usd': ('USD', self.USD_RATE),
            'eur': ('Euro', self.EURO_RATE),
            'rub': ('руб', self.RUB_RATE)
        }
        if currency not in currency_key:
            available_curr = ", ".join(currency_key.keys())
            raise ValueError(
                f'Валюта недоступна, выберите другую: {available_curr}')
        currency_name, currency_rate = currency_key[currency]
        cash_remained = round(cash_remained / currency_rate, 2)
        if cash_remained > 0:
            return (f'На сегодня осталось {cash_remained} {currency_name}')
        cash_remained = abs(cash_remained)
        return ('Денег нет, держись: твой долг - '
                f'{cash_remained} {currency_name}')


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        calories_remained = round(self.get_today_remainder(), 2)
        if calories_remained > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей'
                    f' калорийностью не более {calories_remained} кКал')
        return 'Хватит есть!'


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        self.date = (dt.date.today() if date is None
                     else dt.datetime.strptime(date, '%d.%m.%Y').date())
