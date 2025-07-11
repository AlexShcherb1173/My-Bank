# <u>Проект "Мой банк"</u>
## Описание:
Проект "Мой Банк" - это бэкенд разработка для IT-отдела крупного банка, который делает новую функцию для личного кабинета клиента. Это виджет, который показывает несколько последних успешных банковских операций клиента. 
# Модули проекта:
## **_Пакет masks_**
- get_mask_card_number(card_num_in: str) -> str:  
    Функция принимает строку с 16 цифрами номера карты и вовращает строку маску номера карты
     по 4 цифры через пробел, с 6й по 12ю цифру замена на * <br>
 _Примеры работы:_  
 _7000432156781234 #входной аргумент  
 7000 43** **** 1234 #выход функции_  

- get_mask_acount(acount_num_in: str) -> str:  
    Функция принимает строку с цифрами номера счета и вовращает строку маску номера счета
         последние 4 цифры и две * перед ними  
 _Примеры работы:_  
 _43567896432456 #входной аргумент  
 **2456 #выход функции_
## **_Пакет widget_**
- mask_account_card(card_account_number: str) -> str:  
    Функция принимает строку с названием и номером карты или счета и возвращает строку соответсnвующей
    маски номера карты или счета   
 _Примеры работы:   
  для карты  
   VisaPlatinum 7000792289606361  #входной аргумент  
   Visa Platinum 7000 79** **** 6361  #выход функции  
  для счета  
   Счет 73654108430135874305  #входной аргумент  
   Счет **4305  #выход функции_  <br>

- get_date(date_time_in: str) -> str:  
    Функция принимает строку установленного формата с датой и временем и вовращает строку даты
    в формате дд.мм.гггг  
 _Примеры работы:  
   2024-03-11T02:26:18.671407 #входной аргумент  
   11.03.2024 #выход функции_  
## **_Пакет processing_**
- filter_by_state(list_dict: list, state_in="EXECUTED") -> list:  
    Функция принимает список словарей из 3х полей id, state, date и возвращает список
    словарей-выборку по полю state  
  _Примеры работы:_  
   _Есть список аккаунтов_  
  _[
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}_  
  ]_  
  _Пример по сортировке по полю 'state'  
  [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},   
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
    ]_

- sort_by_date(list_dict: list, reverse=True) -> list:  
    Функция принимает список словарей из 3х полей id, state, date и возвращает список
    словарей сортированных по date(назад или вперед)  
 _Примеры работы:_  
  _Есть список аккаунтов_    
  _[
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
  ]_  
  _Пример сортировки по дате по убыванию_    
  _[
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},   
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},  
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
  ]_  
## **_Пакет generators_**  
- filter_by_currency(transactions:list[dict], currency:str): -> Iterable:  
     функция, которая принимает на вход список словарей, представляющих транзакции возвращает итератор,  
     который поочередно выдает транзакции, где валюта операции соответствует заданной (например, USD). 
_Примеры работы:_
usd_transactions = filter_by_currency(transactions, "USD")  
for _ in range(2):  
    print(next(usd_transactions))  

    {"id": 939719570,  
          "state": "EXECUTED",  
          "date": "2018-06-30T02:08:58.425572",  
          "operationAmount": {  
              "amount": "9824.07",  
              "currency": {  
                  "name": "USD",  
                  "code": "USD"  
              }  
          },  
          "description": "Перевод организации",  
          "from": "Счет 75106830613657916952",  
          "to": "Счет 11776614605963066702"  
      }  
      {  
              "id": 142264268,  
              "state": "EXECUTED",  
              "date": "2019-04-04T23:20:05.206878",  
              "operationAmount": {  
                  "amount": "79114.93",  
                  "currency": {  
                      "name": "USD",  
                      "code": "USD"  
                  }  
              },  
              "description": "Перевод со счета на счет",  
              "from": "Счет 19708645243227258542",  
              "to": "Счет 75651667383060284188"  
}
- transaction_descriptions(transaction_des: list[dict]) -> Iterable:  
    Генератор принимает список словарей с транзакциями и возвращает описание каждой операции по очереди  
_Пример работы:_  
descriptions = transaction_descriptions(transactions)  
for _ in range(5):  
    print(next(descriptions))  

    Перевод организации
    Перевод со счета на счет
    Перевод со счета на счет
    Перевод с карты на карту
    Перевод организации
 
- card_number_generator(start: str = '1', stop: str = '9999999999999999') -> str:  
     Функция принимает начальное и конечное значения для генерации диапазона номеров и
     генерирует номера банковских карт в формате номера карт в заданном диапазоне
     от 0000 0000 0000 0001 до 9999 9999 9999 9999.  
_Примеры работы:_  
for card_number in card_number_generator(1, 5):  
    print(card_number)

   0000 0000 0000 0001  
   0000 0000 0000 0002  
   0000 0000 0000 0003  
   0000 0000 0000 0004  
   0000 0000 0000 0005  


Проверка входящих аргументов функций будет реализована отдельной функцией при сборке проекта,
согласно принципам структурированного программирования

## Тестирование:
Модуль get_mask_card_number

test_masks_.py::test_get_mask_card_number[1111222233334444-1111 22** **** 4444] PASSED [ 12%]
test_masks_.py::test_get_mask_card_number[4444333322221111-4444 33** **** 1111] PASSED [ 25%]
test_masks_.py::test_get_mask_card_number[1234567890123456-1234 56** **** 3456] PASSED [ 37%]
test_masks_.py::test_get_mask_card_number[11112222333344445-1111 22** **** 4444] PASSED [ 50%]
test_masks_.py::test_get_mask_card_number[111122223333444-1111 22** **** 444] PASSED [ 62%]
test_masks_.py::test_get_mask_card_number[111abc22333344sd-111a bc** **** 44sd] PASSED [ 75%]
test_masks_.py::test_get_mask_card_number[111abc2244sd-111a bc** **** ] PASSED [ 87%]
test_masks_.py::test_get_mask_card_number[-   ] PASSED                   [100%]

Модуль get_mask_acount

test_masks_.py::test_get_mask_acount[1111222233334444-**4444] PASSED     [ 14%]
test_masks_.py::test_get_mask_acount[4444333322221111-**1111] PASSED     [ 28%]
test_masks_.py::test_get_mask_acount[1234567890123456-**3456] PASSED     [ 42%]
test_masks_.py::test_get_mask_acount[12345-**2345] PASSED                [ 57%]
test_masks_.py::test_get_mask_acount[12345678900987654321-**4321] PASSED [ 71%]
test_masks_.py::test_get_mask_acount[1234567890098765aaaa-**aaaa] PASSED [ 85%]
test_masks_.py::test_get_mask_acount[-**] PASSED                         [100%]

Модуль mask_account_card

test_widget.py::test_mask_account_card[Maestro1596837868705199-Maestro1596 83** **** 5199] PASSED [ 12%]
test_widget.py::test_mask_account_card[\u0421\u0447\u0435\u0442 64686473678894779589-\u0421\u0447\u0435\u0442 **9589] PASSED [ 25%]
test_widget.py::test_mask_account_card[MasterCard 7158300734726758-MasterCard 7158 30** **** 6758] PASSED [ 37%]
test_widget.py::test_mask_account_card[\u0421\u0447\u0435\u044235383033474447895560-\u0421\u0447\u0435\u0442 **5560] PASSED [ 50%]
test_widget.py::test_mask_account_card[VisaClassic6831982476737658-VisaClassic6831 98** **** 7658] PASSED [ 62%]
test_widget.py::test_mask_account_card[Visa Platinum8990922113665229-Visa Platinum8990 92** **** 5229] PASSED [ 75%]
test_widget.py::test_mask_account_card[VisaGold 5999414228426353-VisaGold 5999 41** **** 6353] PASSED [ 87%]
test_widget.py::test_mask_account_card[\u0441\u0447\u0435\u0442  73654108430135874305-\u0421\u0447\u0435\u0442 **4305] PASSED [100%]

Модуль get_date

test_widget.py::test_get_date[2024-03-11T02:26:18.671407-11.03.2024] PASSED [ 25%]
test_widget.py::test_get_date[2025-06-30T02:-30.06.2025] PASSED          [ 50%]
test_widget.py::test_get_date[2025-07-01-01.07.2025] PASSED              [ 75%]
test_widget.py::test_get_date[2021-01-01rkuryflfkhfglf-01.01.2021] PASSED [100%]

Тестированием установлено что модули корректно обрабатывают корректные входные данные,  
а некорректные данные не вызывают фатальных ошибок.

Модуль filter_by_state и
Модуль sort_by_date
при поступлении некорректных данных, отсутствия соответствующих полей,  
вызывается ошибка KeyError

Модуль filter_by_currency(transactions, "RUB")

{'id': 873106923, 'state': 'EXECUTED', 'date': '2019-03-23T01:09:46.296404', 'operationAmount': 
       {'amount': '43318.34', 'currency': 
             {'name': 'руб.', 'code': 'RUB'}}, 
   'description': 'Перевод со счета на счет', 'from': 'Счет 44812258784861134719', 
   'to': 'Счет 74489636417521191160'}
{'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689', 'operationAmount': 
       {'amount': '67314.70', 'currency': 
             {'name': 'руб.', 'code': 'RUB'}}, 
   'description': 'Перевод организации', 'from': 'Visa Platinum 1246377376343588', 
   'to': 'Счет 14211924144426031657'}  
При отсутствии искомого типа валюты или пустом списке ошибки не возникает.

Модуль transaction_descriptions

Перевод организации
Перевод со счета на счет
Перевод со счета на счет
Перевод организации
Перевод организации
При отсутствии соответствующего поля возвращается None

Модуль card_number_generators

test_generators.py::test_card_number_generator[1, 1, 0000 0000 0000 0001] PASSED [ 20%]
test_generators.py::test_card_number_generator[1111111111111111, 1111111111111111, 1111 1111 1111 1111] PASSED [ 40%]
test_generators.py::test_card_number_generator[9999999999999999, 9999999999999999, 9999 9999 9999 9999] PASSED [ 60%]
test_generators.py::test_card_number_generator[1111222233334444, 1111222233334444, 1111 2222 3333 4444] PASSED [ 80%]
test_generators.py::test_card_number_generator[123456789012345, 123456789012345, 0123 4567 8901 2345] PASSED [100%]

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

