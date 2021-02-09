from __future__ import annotations

import datetime as dt


class Calculator:
    def __init__(self, limit: float) -> None:
        self.limit = limit
        self.records = []

    def add_record(self, record: Record) -> None:
        self.records.append(record)

    def get_today_stats(self) -> float:
        date_today = dt.date.today()
        return round(sum(i.amount for i in self.records
                         if i.date == date_today), 2)

    def get_today_remainder(self) -> float:
        return round((self.limit - self.get_today_stats()), 2)

    def get_week_stats(self) -> float:
        date_today = dt.date.today()
        last_week = date_today - dt.timedelta(days=6)
        return round(sum(i.amount for i in self.records
                         if last_week <= i.date <= date_today), 2)


class CashCalculator(Calculator):
    USD_RATE = 64.78
    EURO_RATE = 89.51
    RUB_RATE = 1.00

    def get_today_cash_remained(self, currency: str) -> str:
        currency_key = {
                         'usd': ('USD', CashCalculator.USD_RATE),
                         'eur': ('Euro', CashCalculator.EURO_RATE),
                         'rub': ('руб', CashCalculator.RUB_RATE),
                         }
        if not(currency in currency_key.keys()):
            raise ValueError('Валюта недоступна, выберите другую: '
                             f'{", ".join(currency_key.keys())}')
        cash_remained = round(self.get_today_remainder() /
                              currency_key[currency][1], 2)
        if cash_remained > 0:
            return ('На сегодня осталось '
                    f'{cash_remained} {currency_key[currency][0]}')
        if not cash_remained:
            return 'Денег нет, держись'
        cash_remained = abs(cash_remained)
        return ('Денег нет, держись: твой долг - '
                f'{cash_remained} {currency_key[currency][0]}')


class CaloriesCalculator(Calculator):
    def get_calories_remained(self) -> str:
        calories_remained = self.get_today_remainder()
        if calories_remained > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей'
                    f' калорийностью не более {calories_remained} кКал')
        return 'Хватит есть!'


class Record:
    def __init__(self, amount: float, comment: str,
                 date=None) -> None:
        self.amount = amount
        self.comment = comment
        self.date = (dt.date.today() if date is None
                     else dt.datetime.strptime(date, '%d.%m.%Y').date())
