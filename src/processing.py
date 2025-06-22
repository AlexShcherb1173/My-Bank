import widget

def filter_by_state(list_dict: list, state_in="EXECUTED") -> list:
    list_dict_filer = []
    for i in list_dict:
        if i["state"] == state_in:
            list_dict_filer.append(i)

    return list_dict_filer


def sort_by_date(list_dict_date: list, reverse=True) -> list:
    if reverse:
        list_dict_date_sort = sorted(list_dict_date, key=lambda id:id["date"], reverse=True)
    else:
        list_dict_date_sort = sorted(list_dict_date, key=lambda id: id["date"], reverse=False)
    return list_dict_date_sort