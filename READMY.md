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

# Модуль Transform_Data

Модуль выполняет различные преобразования данных транзакций, поступающих из разных форматов (CSV, JSON и др.), а также форматирует данные для удобного чтения.

---

## Функции модуля

### `transform_csv(input_dict: dict) -> dict`

Преобразует данные из формата списка словарей, полученного из CSV, в классический словарь с корректными типами для числовых полей.

- **Вход:** словарь с одной парой ключ-значение, где ключ и значение — строки с полями и данными, разделёнными `;`.
- **Выход:** словарь с правильными типами значений.

---

### `transform_json(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]`

Преобразует список транзакций из JSON в формат, совместимый с CSV и XLSX, с проверкой обязательных полей и фильтрацией некорректных записей.

---

### `replace_nan_with_zero(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]`

Заменяет значения `NaN` в списке словарей на строку `"0"` для корректной обработки данных.

---

### `format_transactions(transactions: List[Dict]) -> str`

Преобразует список транзакций в читабельный текстовый формат с датой, описанием, замаскированными номерами счетов и суммами.

---

## Пример использования

```python
from transform_data import transform_csv, transform_json, replace_nan_with_zero, format_transactions

# Пример данных CSV (в виде словаря)
csv_input = {
    "id;amount;date": "123;1500;2023-07-01"
}
csv_data = transform_csv(csv_input)

# Пример данных JSON
json_transactions = [
    {
        "id": "1",
        "state": "EXECUTED",
        "date": "2023-07-01T12:00:00",
        "operationAmount": {"amount": "1500", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод",
        "to": "Счет 1234567890"
    }
]
json_data = transform_json(json_transactions)

# Замена NaN на "0"
clean_data = replace_nan_with_zero(json_data)

# Форматирование для вывода
print(format_transactions(clean_data))
```

# Модуль Reformat_rec

Модуль выполняет преобразования отдельных полей записей в структуре данных транзакций, включая маскирование номеров карт и счетов, а также преобразование формата даты.

---

## Функции модуля

### `get_mask_card_number(card_num_in: str) -> str`

Принимает строку из 16 цифр номера карты и возвращает замаскированный номер в формате:

- Цифры группируются по 4 через пробел.
- С 6-й по 12-ю цифру заменяются на `*`.

**Пример:**

```python
get_mask_card_number("1234567890123456")
# Результат: "1234 5*** **** 3456"
get_mask_acount(acount_num_in: str) -> str
Принимает строку номера счета и возвращает строку с маской:

В начале две звёздочки **.

В конце — последние 4 цифры номера.

Пример:
get_mask_acount("40817810099910004312")
# Результат: "**4312"
mask_account_card(card_account_number: str) -> str
Принимает строку с названием и номером карты или счета и возвращает строку с соответствующей маской:

Если строка начинается с "Счет", применяется маска счета.

Иначе — маскируется номер карты.

get_date(date_time_in: str) -> str
Принимает строку с датой и временем в формате ISO (например, "2023-07-28T14:30:00") и возвращает дату в формате дд.мм.гггг.

Пример:
get_date("2023-07-28T14:30:00")
# Результат: "28.07.2023"
Пример использования

from reformat_rec import get_mask_card_number, get_mask_acount, mask_account_card, get_date

print(get_mask_card_number("1234567890123456"))
print(get_mask_acount("40817810099910004312"))
print(mask_account_card("Счет 40817810099910004312"))
print(mask_account_card("Visa Classic 1234567890123456"))
print(get_date("2023-07-28T14:30:00"))
Зависимости
Python 3.7+ (используются стандартные библиотеки)
```

# Модуль Sort_Data

Модуль для сортировки и фильтрации массива данных (списков словарей) транзакций по различным критериям.

---

## Функции модуля

### `process_bank_search(data: List[Dict], search: str) -> List[Dict]`

Возвращает список записей, у которых в поле `"description"` содержится заданная строка `search`. Поиск нечувствителен к регистру и ищет точные слова.

---

### `filter_and_sort_by_currency(transactions: List[Dict], currency_code: str) -> List[Dict]`

Фильтрует транзакции по заданному коду валюты `currency_code` и возвращает отсортированный по этому коду список.

---

### `filter_by_state(list_dict: List[Dict], state_in: str = "EXECUTED") -> List[Dict]`

Фильтрует список словарей, выбирая записи с указанным состоянием транзакции `state_in` (по умолчанию `"EXECUTED"`).

---

### `sort_by_date(list_dict: List[Dict], reverse: bool = True) -> List[Dict]`

Сортирует список словарей по полю `"date"`. По умолчанию сортирует по убыванию (сначала новые даты), если `reverse=False` — по возрастанию.

---

## Пример использования

```python
from sort_data import process_bank_search, filter_and_sort_by_currency, filter_by_state, sort_by_date

data = [
    {"id": 1, "state": "EXECUTED", "date": "2023-07-28", "description": "Оплата счета", "currency_code": "USD"},
    {"id": 2, "state": "PENDING", "date": "2023-06-15", "description": "Перевод клиенту", "currency_code": "EUR"},
    # ...
]

filtered_by_desc = process_bank_search(data, "Оплата")
filtered_by_currency = filter_and_sort_by_currency(data, "USD")
filtered_by_state = filter_by_state(data, "EXECUTED")
sorted_by_date = sort_by_date(filtered_by_state)

print(filtered_by_desc)
print(filtered_by_currency)
print(sorted_by_date)
Зависимости
Python 3.7+

Стандартные библиотеки: re, typing
```

# Модуль Main

Основной модуль проекта, который объединяет функционал загрузки, преобразования, фильтрации и вывода данных транзакций из разных форматов файлов.

---

## Описание

Модуль реализует:

- Выбор типа исходного файла с транзакциями (`JSON`, `CSV`, `XLSX`)
- Загрузку и преобразование данных в единый формат
- Фильтрацию транзакций по статусу (`state`)
- Сортировку по дате (в прямом или обратном порядке)
- Фильтрацию по валюте (например, рубли)
- Поиск транзакций по ключевому слову в описании
- Очистку данных от пустых или некорректных значений
- Вывод итогового списка транзакций в удобочитаемом формате

---

## Используемые модули

- `input_data` — функции ввода параметров от пользователя
- `reader_data` — чтение данных из файлов JSON, CSV, XLSX
- `transform_data` — преобразование форматов, очистка данных, форматирование вывода
- `sort_data` — фильтрация и сортировка транзакций по разным критериям

---

## Пример запуска

```bash
python main.py
Программа запросит тип файла, статус транзакции, параметры сортировки и фильтрации, а затем выведет список подходящих операций.

Параметры ввода
Тип файла: JSON, CSV, XLSX

Статус транзакции (например, EXECUTED, PENDING и др.)

Сортировка по дате: по убыванию или возрастанию (можно пропустить)

Фильтрация по валюте (например, только RUB)

Поиск по описанию (ввод ключевого слова или пропуск)

Зависимости
Python 3.7+

pandas

Другие стандартные библиотеки: os, sys и др.

Структура проекта

My-Bank/
│
├── data/
│   ├── operations.json
│   ├── transactions.csv
│   └── transactions_excel.xlsx
│
├── src/
│   ├── input_data.py
│   ├── reader_data.py
│   ├── reformat_rec.py
│   ├── sort_data.py
│   ├── transform_data.py
│   └── main.py
│
└── README.md
```

## Установка:

1. Клонируйте репозиторий:
```
git clone https://github.com/AlexShcherb1173/My-Bank
```

2. Установите зависимости:
```
poetry install 
```
3. Запустите main.py  

## Документация:

Дополнительную информацию о структуре проекта и API можно найти в [документации](docs/README.md).
Информация в разработке
## Лицензия:

Проект распространяется под [X11 License](LICENSE).

