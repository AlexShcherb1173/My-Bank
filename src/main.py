import widget
import processing

#date_in = input()

#print(widget.get_date(date_in))

#acount_num_in = input()

#print(widget.mask_account_card(acount_num_in))

a = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]

print(processing.sort_by_date(a))
b = "CANCELED"
print(processing.filter_by_state(a))