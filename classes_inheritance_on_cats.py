"""CREATE FILE cat_data"""

class Cat:
    def __init__(self, name = "", gender = "", age = int):
        self.name = name
        self.gender = gender
        self.age = age

    def gender_is_valid(self):
        gender_is_valid = self.gender
        return self.gender if self.gender == 'Мальчишка' or self.gender == 'Девчонка' else "Так 'Мальчишка' или 'Девчонка'?"

    def age_is_valid(self):
        age_is_valid = self.age
        return self.age if self.age >= 0 else 'не может быть отрицательным числом! Не лукавь в следующий раз, умоляю!'

    def cat_says(self):
        print(self.name + " " + "говорит 'Мяу, родной!")

    def hello_kitty(self):
        print('Кот по имени', self.name, '\nПол шерстяного:', self.gender_is_valid(), '\nВозраст шерстяного: ', self.age_is_valid())
        print(self.cat_says())
   
   
"""CREATE FILE get_some_cats"""

from cat_data import Cat

cat_1 = Cat('Барон', 'Мальчишка', 2)
cat_2 = Cat('Cэм', 'Мальчишка', 2)

print(cat_1.hello_kitty())
print(cat_2.hello_kitty())
