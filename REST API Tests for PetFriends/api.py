import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends1.herokuapp.com/'

        #Забираем ключ АПИ
    def get_api_key(self, email, password):

        headers = {
            'email': email,
            'password': password
        }

        res = requests.get(self.base_url + 'api/key', headers = headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    #Получаем список питомцев
    def get_list_of_pets(self, auth_key, filter):
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter }

        res = requests.get(self.base_url + 'api/pets', headers = headers, params = filter)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    #ПОСТим нового питомца с фотографией
    def post_new_pet(self, auth_key, name, animal_type, age, pet_photo):
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'images/pet_1.jpg')
            })
        headers = {'auth_key': auth_key['key'],
                   'Content-Type': data.content_type}
        res = requests.post(self.base_url + 'api/pets', headers = headers, data = data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    #Обновляем информацию о питомце
    def put_update_pet_info(self, auth_key, pet_id, name, animal_type, age):
        headers = {'auth_key': auth_key['key']}
        data = {'pet_id': pet_id,
                'name': name,
                'animal_type': animal_type,
                'age': age}
        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers = headers, data = data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    #Удаляем питомца
    def delete_goodbye_my_pet(self, auth_key, pet_id):
        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

#Задание 19.7.2

#Используем заведомо неверный ключ для получения списка своих питомцев
    def get_list_of_my_pets_with_invalid_key(self, auth_key, filter):
        headers = {'auth_key': auth_key['ea738148a1f19838e1c5d1413877f3691a3731380e733e877b0ae799']}
        filter = {'filter': filter }

        res = requests.get(self.base_url + 'api/pets', headers = headers, params = filter)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    #ПОСТим нового животного без фотографии
    def post_new_pet_without_photo(self, auth_key, name, animal_type, age):
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    #Публикуем фото к уже существующему питомцу
    def post_photo_of_existing_pet(self, auth_key, pet_id, pet_photo):
        data = MultipartEncoder(
            fields={
                'pet_id': pet_id,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'images/pet_2.jpg')
            })
        headers = {'auth_key': auth_key['key'],
                   'Content-Type': data.content_type}
        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    #Публикуем питомца с возрастом, который указываем в буквах и символах
    def post_new_pet_with_age_in_non_figures(self, auth_key, name, animal_type, age, pet_photo):
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'images/pet_3.jpg')
            })
        headers = {'auth_key': auth_key['key'],
                   'Content-Type': data.content_type}
        res = requests.post(self.base_url + 'api/pets', headers = headers, data = data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    #Пробуем публиковать питомца вообще без какой-либо информации
    def post_new_pet_without_any_info(self, auth_key, name, animal_type, age):
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    #Пробуем публиковать питомца без авторизации
    def post_new_pet_without_auth(self, name, animal_type, age):

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        res = requests.post(self.base_url + 'api/create_pet_simple', data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
