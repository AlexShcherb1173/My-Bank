# masks.py
import os
import logging

# Создание логгера для модуля mmasks
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создание file handler
os.chdir(r'C:\users\alex_\PycharmProjects\My-Bank')
file_handler = logging.FileHandler(r'logs\masks.log', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

# Formatter: время, модуль, уровень, сообщение
file_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

# Привязка форматтера к handler и handler к логгеру
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Добавление handler к логгеру
if not logger.hasHandlers():  # Чтобы избежать дублирования логов
    logger.addHandler(file_handler)

def get_mask_card_number(card_num_in: str) -> str:
    try:
        if not card_num_in or len(card_num_in) < 16 or not card_num_in.isdigit():
            raise ValueError("Invalid card number. Must be at least 16 digits.")

        card_num_mask = ''
        for i in range(len(card_num_in)):
            if 5 < i < 12:
                card_num_mask += '*'
            else:
                card_num_mask += card_num_in[i]

        substring_1 = card_num_mask[:4]
        substring_2 = card_num_mask[4:8]
        substring_3 = card_num_mask[8:12]
        substring_4 = card_num_mask[12:16]

        masked_card = f"{substring_1} {substring_2} {substring_3} {substring_4}"
        logger.debug(f"Успешное маскирование номера карты: {masked_card}")
        return masked_card
    except Exception as e:
        logger.error(f"Ошибка при маскировании номера карты: {e}")
        return "**** **** **** ****"

def get_mask_acount(acount_num_in: str) -> str:
    try:
        if not acount_num_in.isdigit() or len(acount_num_in) < 4:
            raise ValueError("Неверный формат номера счёта")

        masked_acount = '**' + acount_num_in[-4:]
        logger.debug(f"Успешное маскирование номера счёта: {masked_acount}")
        return masked_acount
    except Exception as e:
         logger.error(f"Ошибка при маскировании номера счёта: {e}")
         return '**0000'




