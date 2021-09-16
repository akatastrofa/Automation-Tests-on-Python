from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import pytest

pf = PetFriends()

def generate_string(num):
   return "x" * num

def russian_chars():
   return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

def chinese_chars():
   return '的一是不了人我在有他这为之大来以个中上们'

def special_chars():
   return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'

@pytest.fixture(autouse=True)
def ket_api_key():
    status, pytest.key = pf.get_api_key(valid_email, valid_password)
    assert status == 200
    assert 'key' in pytest.key

    yield

@pytest.mark.parametrize('name', [''], ids=['empty'])
@pytest.mark.parametrize('animal_type', [''], ids=['empty'])
@pytest.mark.parametrize('age', ['', '-1', '0', '100', '1.5', '2147483647', '2147483648',
                                 russian_chars(), russian_chars().upper(), chinese_chars(), special_chars()],
                         ids=['empty', 'negative', 'zero', 'gtm', 'float', 'int_max', 'int_max + 1',
                              'rus', 'RUS', 'chn', 'specials'])
def test_add_new_pet_simple_negative(name, animal_type, age):
    pytest.status, result = pf.add_new_pet_simple(pytest.key, name, animal_type, age)
    assert pytest.status == 400

@pytest.mark.parametrize('name', [generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(),
                                  chinese_chars(), special_chars(), '123'],
                         ids=['255s', 'mt1000s', 'rus', 'RUS', 'chn', 'specials', 'digits'])
@pytest.mark.parametrize('animal_type', [generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(),
                                  chinese_chars(), special_chars(), '123'],
                         ids=['255s', 'mt1000s', 'rus', 'RUS', 'chn', 'specials', 'digits'])
@pytest.mark.parametrize('age', ['1'], ids=['min'])
def test_add_new_pet_simple_positive(name, animal_type, age):
    pytest.status, result = pf.add_new_pet_simple(pytest.key, name, animal_type, age)
    assert pytest.status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age

@pytest.mark.parametrize('name', [''], ids=['empty'])
@pytest.mark.parametrize('animal_type', [''], ids=['empty'])
@pytest.mark.parametrize('age', ['', '-1', '0', '100', '1.5', '2147483647', '2147483648',
                                 russian_chars(), russian_chars().upper(), chinese_chars(), special_chars()],
                         ids=['empty', 'negative', 'zero', 'gtm', 'float', 'int_max', 'int_max + 1',
                              'rus', 'RUS', 'chn', 'specials'])
@pytest.mark.parametrize('pet_photo', ['', 'images/txtfile.txt', 'images/pet_4.ghf'],
                         ids=['empty', 'txt file', 'broken'])
def test_add_new_pet_with_photo_negative(name, animal_type, age, pet_photo):
    pytest.status, result = pf.post_new_pet(pytest.key, name, animal_type, age, pet_photo)
    assert pytest.status == 400 or 500
    print(pytest.status)

@pytest.mark.parametrize('name', [generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(),
                                  chinese_chars(), special_chars(), '123'],
                         ids=['255s', 'mt1000s', 'rus', 'RUS', 'chn', 'specials', 'digits'])
@pytest.mark.parametrize('animal_type', [generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(),
                                  chinese_chars(), special_chars(), '123'],
                         ids=['255s', 'mt1000s', 'rus', 'RUS', 'chn', 'specials', 'digits'])
@pytest.mark.parametrize('age', ['1'], ids=['min'])
@pytest.mark.parametrize('pet_photo', ['images/pet_1.jpg'], ids=['correct photo'])
def test_add_new_pet_with_photo_positive(name, animal_type, age, pet_photo):
    pytest.status, result = pf.post_new_pet(pytest.key, name, animal_type, age, pet_photo)
    assert pytest.status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age
    print(pytest.status)

@pytest.mark.parametrize('pet_id', ['', generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(),
                                    chinese_chars(), special_chars(), '123'],
                         ids=['empty', '255s', 'mt1000s', 'rus', 'RUS', 'chn', 'specials', 'digits'])
@pytest.mark.parametrize('pet_photo', ['', 'images/txtfile.txt', 'images/pet_4.ghf'],
                         ids=['empty', 'txt file', 'broken'])
def test_add_pet_photo_negative(pet_id, pet_photo):
    pytest.status, result = pf.add_photo_of_existing_pet(pytest.key, pet_id, pet_photo)
    assert pytest.status == 400 or 500

@pytest.mark.parametrize('pet_id', ['d5f092fa-1da0-43b3-a08f-f13b2aa7183d'], ids=['correct pet id'])
@pytest.mark.parametrize('pet_photo', ['images/pet_2.jpg'], ids=['correct photo'])
def test_add_pet_photo_positive(pet_id, pet_photo):
    pytest.status, result = pf.add_photo_of_existing_pet(pytest.key, pet_id, pet_photo)
    assert pytest.status == 200
    assert result['id'] == pet_id
    print(pytest.status, result)


@pytest.mark.parametrize('content_type', ['application/json'], ids=['json'])
@pytest.mark.parametrize('name', [generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(),
                                  chinese_chars(), special_chars(), '123'],
                         ids=['255s', 'mt1000s', 'rus', 'RUS', 'chn', 'specials', 'digits'])
@pytest.mark.parametrize('animal_type', [generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(),
                                  chinese_chars(), special_chars(), '123'],
                         ids=['255s', 'mt1000s', 'rus', 'RUS', 'chn', 'specials', 'digits'])
@pytest.mark.parametrize('age', ['1'], ids=['min'])
def test_add_new_pet_simple_with_headers_positive(content_type, name, animal_type, age):
    pytest.status, result = pf.add_new_pet_simple_with_headers(pytest.key, content_type, name, animal_type, age )
    assert content_type == 'application/json'
    print(pytest.status)









