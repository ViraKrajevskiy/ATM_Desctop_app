# from Backend.functions.translate.TranslateMenu import select_language
#
# def see_course_and_change():
#
#
#     lang = select_language()
#
#     while True:
#         data = translations[lang]
#
#         for item in data['SeeCourseMenu']:
#             print(f'')
#
#         user_inputs = int(input())
#
#         if user_inputs == 1:
#
from Backend.data_base.database import db
from Backend.functions.see_course_mon.course_rater_func import CurrencyRate, start_currency_simulation
from Backend.functions.translate.TranslateMenu import select_language, translations


def get_latest_rate(currency_pair: str) -> float:
    rate_obj = (CurrencyRate
                .select()
                .where(CurrencyRate.currency_pair == currency_pair)
                .order_by(CurrencyRate.timestamp.desc())
                .first())
    return rate_obj.rate if rate_obj else None

currency_simulation_started = False

def see_course_and_change(lang):

    global currency_simulation_started

    if not currency_simulation_started:
        start_currency_simulation()
        currency_simulation_started = True

    # Подключение к БД, если не подключена
    if db.is_closed():
        db.connect()

    while True:
        data = translations[lang]
        print()
        print("=== Курсы валют ===")
        usd = get_latest_rate("SUM->USD")
        rub = get_latest_rate("SUM->RUB")
        eur = get_latest_rate("SUM->EUR")

        print(f"{data['SeeCourseMenu'][0]} {usd} UZS")   # Курс сум - доллар.
        print(f"{data['SeeCourseMenu'][1]} {rub} UZS")   # Курс сум - рубль.
        print(f"{data['SeeCourseMenu'][2]} {eur} UZS")   # Курс сум - евро.

        print(data['SeeCourseMenu'][3])  # 1. Обменять валюту.
        print(data['SeeCourseMenu'][4])  # 2. Выйти в главное меню.
        print(data['SeeCourseMenu'][5])  # 3. Выйти из программы.

        try:
            user_input = int(input(data['ChooseValue']))

            if user_input == 1:
                print(">> Функция обмена валюты пока не реализована.")
            elif user_input == 2:
                break
            elif user_input == 3:
                print(data['Exit'])
                exit(0)
            else:
                print(data['InvalidOptionRange'])

        except ValueError:
            print(data[''])
