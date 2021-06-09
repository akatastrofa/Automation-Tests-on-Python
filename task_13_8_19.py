tickets = int(input("How many tickets are you about to buy, bruh? ")) # an amount of tickets
money = 0 # a variable, we use for the ticket price

for one_dude in range(tickets): # we spin the cycle
    age = int(input("How old's that dude? ")) # here comes our 'age' variable
    if age < 18:
        money += 0 # a ticket price depends on age
    if 18 <= age <= 25:
        money += 990
    if age > 25:
        money += 1390
if tickets > 3: # we check an amount of tickets and introduce a discount condition
    money = money - (money * 0.1)
print("It's {} rubles including 10 % discount, bruh".format(money)) # here comes the bill
