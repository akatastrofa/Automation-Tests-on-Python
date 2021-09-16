import sys
sys.path.append('/Users/Andris/PycharmProjects/petfriendsAPItests/')
from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import pytest

pf = PetFriends()

class Test_PF:
    @pytest.fixture(autouse=True)
    def get_key(self):
        self.pf = PetFriends()
        status, self.key = self.pf.get_api_key(valid_email, valid_password)
        assert status == 200
        assert 'key' in self.key

        yield

        assert self.status == 200

    @pytest.mark.api
    @pytest.mark.auth
    def test_get_my_pets(self, filter=''):  # filter available values : my_pets
        self.status, result = self.pf.get_list_of_pets(self.key, filter)
        assert len(result['pets']) > 0
        print(self.status)
        pass

    @pytest.mark.api
    @pytest.mark.event
    def test_post_my_new_pet(self, name = 'Staki', animal_type = 'stakan', age = '50', pet_photo = 'images/pet_2.jpg'):
        self.status, result = self.pf.post_new_pet(self.key, name, animal_type, age, pet_photo)
        assert result['name'] == name
        print(self.status, result['name'])

    @pytest.mark.xfail
    @pytest.mark.api
    @pytest.mark.event
    def test_put_pet_update(self, pet_id = '1ecb0240-e371-4f9b-91ae-7217f1ed5250', name = 'Meh', animal_type = 'glass', age = 16):
        self.status, result = self.pf.put_update_pet_info(self.key, pet_id, name, animal_type, age)
        assert result['name']
        print(self.status, result['name'], result['animal_type'], result['age'])

    @pytest.mark.skip(reason = 'Не нужно удалять')
    def test_delete_my_pet(self, pet_id = '295d1e22-beae-4bd3-a321-853126da450c'):
        self.status, result = self.pf.delete_goodbye_my_pet(self.key, pet_id)
        my_pets = self.pf.get_list_of_pets(self.key, 'my_pets')
        assert pet_id not in my_pets
        print(my_pets)