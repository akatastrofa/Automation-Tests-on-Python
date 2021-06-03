money = int(input('How much money would you like to invest?'))

# dict with %
per_cent = {'ТКБ': 5.6, 'СКБ': 5.9, 'ВТБ': 4.28, 'СБЕР': 4.0}
deposit = []
for value in per_cent.values():
    result = float(money/100*value)
    deposit.append(result)
print(deposit)