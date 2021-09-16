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

@pytest.mark.parametrize('filter', [generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(),
                          chinese_chars(), special_chars(), 123],
                         ids=['255s', 'mt1000s', 'rus', 'RUS', 'chn', 'specials', 'digits'])
def test_get_my_pets_with_negative_filter(filter):
    pytest.status, result = pf.get_list_of_pets(pytest.key, filter)
    assert pytest.status == 500
    print(pytest.status, result)

@pytest.mark.parametrize('filter', ['', 'my_pets'], ids=['empty string', 'only my pets'])
def test_get_all_pets_with_valid_key(filter):
    pytest.status, result = pf.get_list_of_pets(pytest.key, filter)
    assert pytest.status == 200
    assert len(result['pets']) > 0