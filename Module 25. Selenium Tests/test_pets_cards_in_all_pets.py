import pytest
from selenium import webdriver

@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Firefox(executable_path='/Users/Andris/PycharmProjects/drivers/geckodriver')
    # Добавляем неявное ожидание
    pytest.driver.implicitly_wait(5)
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends1.herokuapp.com/login')

    yield

    pytest.driver.quit()

def test_show_all_pets():
    # Вводим логин и пароль
    pytest.driver.find_element_by_id('email').send_keys('hjkhd667oo@hohoho.ya')
    pytest.driver.find_element_by_id('pass').send_keys('iuuklpiu777896Ty')
    # Нажимаем на кнопку входа
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице
    assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"
    # Переменные для поиска фото, имён и описаний (вид, возраст) питомцев на карточках
    images = pytest.driver.find_elements_by_css_selector('.card-deck .card-img-top')
    names = pytest.driver.find_elements_by_css_selector('.card-deck .card-title')
    descriptions = pytest.driver.find_elements_by_css_selector('.card-deck .card-text')

    for i in range(len(names)):
        # Проверяем, что у всех питомцев есть фото
        assert images[i].get_attribute('src') != ''
        # Проверяем, что у всех питомцев есть имена
        assert names[i].text != ''
        # Проверяем, что у всех питомцев есть описания
        assert descriptions[i].text != ''
        parts = descriptions[i].text.split(', ')
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0
