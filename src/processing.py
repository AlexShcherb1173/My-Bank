def filter_by_state(list_dict: list[dict], state_in: str = "EXECUTED") -> list[dict]:
    """Функция принимает список словарей из 3х полей id, state, date и возвращает список
    словарей-выборку по полю state"""
    list_dict_filer_state = []
    for account in list_dict:
        if account["state"] == state_in:
            list_dict_filer_state.append(account)
    return list_dict_filer_state


def sort_by_date(list_dict: list[dict], reverse: bool = True) -> list[dict]:
    """Функция принимает список словарей из 3х полей id, state, date и возвращает список
    словарей сортированных по date(назад или вперед)"""
    if reverse:
        list_dict_sort_by_date = sorted(list_dict, key=lambda id: id["date"], reverse=True)
    else:
        list_dict_sort_by_date = sorted(list_dict, key=lambda id: id["date"], reverse=False)
    return list_dict_sort_by_date
