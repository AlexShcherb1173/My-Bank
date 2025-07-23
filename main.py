

print ('''Привет! Добро пожаловать в программу работы с банковскими транзакциями.
Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла/n'''
)
inp_form = input ()
def input_choice(i):
    i = int(i)
    if i == 1:
        ch = 'json'
    elif i == 2:
        ch = 'csv'
    elif i == 3:
         ch = "xlsx"
    else:
         ch = 'incorrect input'
    return ch

print (f"для обработки выбран {input_choice(inp_form)}")
print('''Введите статус, по которому необходимо выполнить фильтрацию. \n
Доступные cтатусы: EXECUTED, CANCELED, PENDING''')
filtre_state = input()