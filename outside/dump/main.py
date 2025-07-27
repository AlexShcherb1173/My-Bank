# Модуль Main
# Модуль собирает весь функционал в реализацию

from input_data import *
from reader_data import *
from sort_data import *
from transform_data import *

# ____________________________основной код обернутый в функцию ----------------------------------------------------
def main() -> None:
    os.chdir(r"C:\Users\alex_\PycharmProjects\My-Bank")
    # пути к тестовым файлам
    filepath_json = r"data\operations.json"
    filepath_csv = r"data\transactions.csv"
    filepath_xlsx = r"data\transactions_excel.xlsx"

    # ввод типа файлов данных
    choice = input_choice()
    print(f"для обработки выбран {choice} файл")

    # загрузка соответствующего файла в таблицу транзакций
    if choice == "json":
        transaction_table_json = read_json_file(filepath_json)
        transaction_table = transform_json(transaction_table_json)
    elif choice == "csv":
        transaction_table = read_transactions_from_csv(filepath_csv)
    elif choice == "xlsx":
        transaction_table = read_transactions_from_excel(filepath_xlsx)

    # фильтрация по категории
    f_state_transac_tab = filter_by_state(transaction_table, input_state())

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
    if input_descr():
        f_state_date_currency_descr_tab = process_bank_search(
            f_state_date_currency_tab, input("Введите слово для поиска: \n")
        )
    else:
        f_state_date_currency_descr_tab = f_state_date_currency_tab

    # очистка таблицы от пустых записей
    f_state_date_currency_descr_tab_clean = replace_nan_with_zero(f_state_date_currency_descr_tab)

    # вывод результата
    print(f"Всего банковских операций в выборке {len(f_state_date_currency_descr_tab_clean)}\n")
    print(format_transactions(f_state_date_currency_descr_tab_clean))


# ---------------------------------------------------------------------------------------------------------------------


# -----------------------------------------main tests------------------------------------------------------------------
if __name__ == "__main__":
    main()
