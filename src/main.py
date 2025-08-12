# Модуль Main
# Модуль собирает весь функционал в реализацию

import os
import sys
import pandas as pd
sys.path.append(os.path.abspath("src"))
from src.input_data import input_choice, input_descr, input_sort_currency, input_sort_date, input_state
from src.reader_data import read_json_file, read_transactions_from_csv, read_transactions_from_excel
from src.sort_data import filter_and_sort_by_currency, filter_by_state, process_bank_search, sort_by_date
from src.transform_data import format_transactions, replace_nan_with_zero, transform_json, transform_csv


# ____________________________основной код обернутый в функцию ----------------------------------------------------
def main() -> None:
    os.chdir(r"C:\Users\alex_\PycharmProjects\My-Bank")
    # пути к тестовым файлам
    filepath_json = r"data\operations.json"
    filepath_csv = r"data\transactions.csv"
    filepath_xlsx = r"data\transactions_excel.xlsx"

    # ввод типа файлов данных
    choice = input_choice()
    print(f"\033[4mПрограмма:\033[0m Для обработки выбран {choice}-файл")

    # загрузка соответствующего файла в таблицу транзакций
    if choice == "JSON":
        transaction_table_json = read_json_file(filepath_json)
        transaction_table = transform_json(transaction_table_json)
    elif choice == "CSV":
        transaction_table = read_transactions_from_csv(filepath_csv)
    elif choice == "XLSX":
        transaction_table = read_transactions_from_excel(filepath_xlsx)

    # фильтрация по категории
    state = input_state()
    f_state_transac_tab = filter_by_state(transaction_table, state)
    print(f'\033[4mПрограмма:\033[0m Операции отфильтрованы по статусу "{state}"')
    # фильтрация по дате по запросу
    date_param = input_sort_date()
    if date_param[0]:
        f_state_date_transac_tab = sort_by_date(f_state_transac_tab, date_param[1])
    else:
        f_state_date_transac_tab = f_state_transac_tab

    # фильтрация рублевых транзакций по запросу
    if input_sort_currency():
        f_state_date_currency_tab = filter_and_sort_by_currency(f_state_date_transac_tab, "RUB")
    else:
        f_state_date_currency_tab = f_state_date_transac_tab

    # фильтрация по описанию по запросу
    word_descr = input_descr()
    if word_descr[0] == "да":
        f_state_date_currency_descr_tab = process_bank_search(f_state_date_currency_tab, word_descr[1])
    elif word_descr[0] == "нет":
        f_state_date_currency_descr_tab = f_state_date_currency_tab

    # очистка таблицы от пустых записей
    f_state_date_currency_descr_tab_clean = replace_nan_with_zero(f_state_date_currency_descr_tab)

    # вывод результата
    if len(f_state_date_currency_descr_tab_clean) == 0:
        print("\033[4mПрограмма:\033[0m Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(
         f"\033[4mПрограмма:\033[0m Всего банковских операций в выборке {len(f_state_date_currency_descr_tab_clean)}\n"
        )
        print(format_transactions(f_state_date_currency_descr_tab_clean))


# ---------------------------------------------------------------------------------------------------------------------


# -----------------------------------------main tests------------------------------------------------------------------
if __name__ == "__main__":
    main()
