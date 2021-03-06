from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import pytest
from requests_toolbelt.multipart.encoder import MultipartEncoder

pf = PetFriends()

#Тестируем получение АПИ ключа с верными пользовательскими данными
def test_get_api_key_for_valid_user(email = valid_email, password = valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

    #Получаем список своих питомцев с верным АПИ ключом
def test_get_all_pets_with_valid_key(filter = ''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

    #Публикуем нового питомца с фотографией
def test_post_new_pet_with_valid_data(name = 'Корешок', animal_type = 'frog', age = '56', pet_photo = 'images/pet_1.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

    #Изменяем информацию о существующем питомце
def test_put_update_pet_info(name = 'Захар', animal_type = 'zhabina', age = '60'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) > 0:
        status, result = pf.put_update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception('Нет у тебя такого животного, ты сам животное')

        #Удаляем питомца и прощаемся с ним
def test_delete_goodbye_my_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_goodbye_my_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

#Задание 19.7.2: составить 10 тестов
#Используем для получения ключа неверные пользовательские данные
def test_get_api_key_for_invalid_user(email = invalid_email, password = invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

    #Пробуем получить список своих питомцев с заведомо неверным АПИ ключом
def test_get_list_of_my_pets_with_invalid_key(filters = ''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_my_pets_with_invalid_key(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

    #Публикуем нового питомца без фото
def test_post_new_pet_without_photo(name = 'Zanussi', animal_type = 'stakan', age = '12'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

    #Публикуем фото к уже существующему питомцу
def test_post_photo_of_existing_pet(pet_photo = 'images/pet_2.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']
    if len(my_pets['pets']) > 0:
        status, result = pf.post_photo_of_existing_pet(auth_key, pet_id, pet_photo)
        assert status == 200
        assert result['id'] == pet_id
    else:
        raise Exception('Нет у тебя такого животного, ты сам животное')

    #Пробуем изменять информацию к несуществующему питомцу
def test_put_update_info_for_nonex_pet(name = 'Керзак', animal_type = 'паразит', age = '103'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][20]['id']
    if len(my_pets['pets']) > 0:
        status, result = pf.put_update_pet_info(auth_key, pet_id, name, animal_type, age)
        assert status == 200
        assert result['name'] == name

    #Пробуем вместо цифр в возраст животного вбивать буквы и символы
def test_post_pet_with_age_in_non_figures(name = 'Витёк', animal_type = 'летучка', age = 'семьдесят+', pet_photo = 'images/pet_3.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_new_pet_with_age_in_non_figures(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

    #Пробуем публиковать нового питомца вообще без какой-либо информации
def test_post_new_pet_without_any_info(name = '', animal_type = '', age = ''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_new_pet_without_any_info(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

    #Пробуем удалить несуществующего питомца
def test_delete_nonexisting_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][20]['id']
    status, _ = pf.delete_goodbye_my_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

    #Пробуем вводить в данные существующего питомца большой набор букв, цифр и символов
def test_put_update_pet_info_with_alotta_everything(name = '1q2w3e4r5t6y7u8i9o0p--[ouuhiughsdkghkjdlv%%%%%',\
                                                    animal_type = '00000000009999999987777736636hjgjhgasfas55363663636363636636363', \
                                                    age = '98797987987987987987987000%%%%%%%0000000999999998777773663655363663636363636636363'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']
    if len(my_pets['pets']) > 0:
        status, result = pf.put_update_pet_info(auth_key, pet_id, name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception('Нет у тебя такого животного, ты сам животное')

    #Пробуем получить АПИ ключ с верным имейлом, но неверным паролем
def test_get_api_key_with_valid_email_but_invalid_pass(email = valid_email, password = invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

    #Пробуем опубликовать нового питомца без авторизации
def test_post_new_pet_without_auth(name = 'Patty', animal_type = 'мышь', age = '10'):
    status, result = pf.post_new_pet_without_auth(name, animal_type, age)
    assert status == 200
    assert result['name'] == name
