# <u>Проект "Мой банк"</u>
## Описание:
Проект "Мой Банк" - это бэкенд разработка для IT-отдела крупного банка, который делает новую функцию для личного кабинета клиента. Это виджет, который показывает несколько последних успешных банковских операций клиента. 
# Модули проекта:


# Модуль Input_Data

Модуль `Input_Data` содержит функции для ввода данных пользователем с интерактивной фильтрацией некорректных значений. 

Все функции защищают ввод от ошибок и повторно запрашивают данные, пока пользователь не введёт правильный формат.

---

## Функции модуля

### input_choice() -> str

Запрашивает у пользователя выбор типа файла для работы с банковскими транзакциями:

- 1 — JSON-файл
- 2 — CSV-файл
- 3 — XLSX-файл

Возвращает строку `"JSON"`, `"CSV"` или `"XLSX"`.

---

### input_state() -> str

Запрашивает статус операции для фильтрации:

- EXECUTED
- CANCELED
- PENDING

Возвращает выбранный статус в верхнем регистре.

---

### input_sort_date() -> list

Запрашивает у пользователя, нужно ли сортировать операции по дате, и если да — по возрастанию или убыванию.

Возвращает список из двух элементов:

- Первый — `True` или `False`, нужен ли сортировать.
- Второй — `True`, если сортировать по убыванию, или `False` для возрастания.

---

### input_sort_currency() -> bool

Запрашивает, нужно ли показывать только рублевые транзакции.

Возвращает `True` — только рублевые, `False` — все.

---

### input_descr() -> list

Запрашивает, фильтровать ли транзакции по слову в описании.

Если пользователь отвечает "да", запрашивает ключевое слово.

Возвращает список:

- Первый элемент: `"да"` или `"нет"`.
- Второй элемент: ключевое слово (если есть).

---

## Пример использования

```python
from input_data import input_choice, input_state, input_sort_date, input_sort_currency, input_descr

file_type = input_choice()
print(f"Выбран тип файла: {file_type}")

state = input_state()
print(f"Фильтрация по статусу: {state}")

sort_date = input_sort_date()
print(f"Сортировка по дате: {sort_date}")

only_rub = input_sort_currency()
print(f"Только рублевые транзакции: {only_rub}")

descr_filter = input_descr()
print(f"Фильтрация по описанию: {descr_filter}")
```
# Модуль Reader_Data

Модуль `Reader_Data` предназначен для считывания данных финансовых транзакций из файлов различных форматов: CSV, Excel (XLSX) и JSON.

---

## Функционал модуля

- `read_transactions_from_csv(file_path: str) -> list[dict]`  
  Считывает транзакции из CSV-файла, возвращает список словарей. Использует `transform_csv` для преобразования каждой строки.

- `read_transactions_from_excel(file_path: str) -> list[dict]`  
  Считывает транзакции из Excel-файла (.xlsx), возвращает список словарей с транзакциями.

- `read_json_file(filepath: str) -> list`  
  Считывает транзакции из JSON-файла, возвращает список словарей. Если файл пуст, не существует или некорректен — возвращает пустой список.

---

## Зависимости

- Python 3.7+
- pandas (для чтения Excel файлов)

Установка pandas:

```bash
pip install pandas


from reader_data import read_transactions_from_csv, read_transactions_from_excel, read_json_file

csv_transactions = read_transactions_from_csv("data/transactions.csv")
excel_transactions = read_transactions_from_excel("data/transactions.xlsx")
json_transactions = read_json_file("data/transactions.json")

print(f"CSV transactions: {len(csv_transactions)}")
print(f"Excel transactions: {len(excel_transactions)}")
print(f"JSON transactions: {len(json_transactions)}")
Особенности реализации
Для CSV используется модуль csv.DictReader и функция transform_csv из модуля transform_data для обработки каждой записи.

Для Excel используется pandas.read_excel.

Для JSON реализована обработка ошибок и проверка корректности формата данных.

Модуль автоматически возвращает пустой список при ошибках чтения или отсутствии файла.

Тестирование
Для тестирования функций можно использовать pytest и мокать файловые операции с помощью unittest.mock или библиотеки pytest-mock.

Пример простого теста для JSON чтения:


import pytest
from reader_data import read_json_file

def test_read_json_file_empty(tmp_path):
    file = tmp_path / "empty.json"
    file.write_text("")  # пустой файл
    assert read_json_file(str(file)) == []

def test_read_json_file_invalid(tmp_path):
    file = tmp_path / "invalid.json"
    file.write_text("{bad json}")
    assert read_json_file(str(file)) == []
``` 

