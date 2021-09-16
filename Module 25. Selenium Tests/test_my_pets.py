import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
    # Для работы используем драйвер Firefox
    pytest.driver = webdriver.Firefox(executable_path='/Users/Andris/PycharmProjects/drivers/geckodriver')
    pytest.driver.get('http://petfriends1.herokuapp.com/login')

    yield
    pytest.driver.quit()

    # Проверка авторизации на сайте и вход в аккаунт со своими питомцами
def test_show_my_pets():
    # Вводим логин и пароль
    pytest.driver.find_element_by_id('email').send_keys('hjkhd667oo@hohoho.ya')
    pytest.driver.find_element_by_id('pass').send_keys('iuuklpiu777896Ty')
    # Нажимаем кнопку "Войти"
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    # Проверяем, что мы точно попали на главную страницу
    assert pytest.driver.find_element_by_class_name('navbar-brand').text == 'PetFriends'
    # Нажимаем кнопку "Мои питомцы", чтобы войти в свой аккаунт со списком загруженных на сайт питомцев
    pytest.driver.find_element_by_link_text('Мои питомцы').click()
    # Делаем проверку, что мы находимся в своём аккаунте
    assert pytest.driver.find_element_by_tag_name('h2').text == 'matyuin'

    # Задание 25.3.1

def test_my_pets_got_it():
    # Проходим весь процесс авторизации и входа в свой аккаунт
    pytest.driver.find_element_by_id('email').send_keys('hjkhd667oo@hohoho.ya')
    pytest.driver.find_element_by_id('pass').send_keys('iuuklpiu777896Ty')
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    pytest.driver.find_element_by_link_text('Мои питомцы').click()
    assert pytest.driver.find_element_by_tag_name('h2').text == 'matyuin'

    # Переменная с количеством питомцев, которое даёт нам статистика в аккаунте
    what_i_got = 6
    # Переменная с явным ожиданием для вычисления количества питомцев из таблицы в аккаунте
    actual_pets_amount = WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_all_elements_located((By.XPATH, '//tbody/tr')))
    # Пустой список для питомцев с фото
    pets_with_photo = []
    # Переменная с явным ожиданием для поиска фото, имён, возрастов и пород питомцев на странице
    photos = WebDriverWait(pytest.driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//th/img')))
    pet_names = WebDriverWait(pytest.driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//td[1]')))
    pet_ages = WebDriverWait(pytest.driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//td[2]')))
    pet_breeds = WebDriverWait(pytest.driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//td[3]')))
    # Пункт 1: Присутствуют все питомцы
    assert len(actual_pets_amount) == what_i_got
    # Пункт 2: Хотя бы у половины питомцев есть фото
    for i in range(len(actual_pets_amount)):
        if photos[i].get_attribute('src') != '':
            pets_with_photo.append(i)
        return pets_with_photo
    assert len(pets_with_photo) >= actual_pets_amount / 2
    # Пункт 3: У всех питомцев есть имя, возраст и порода
    for i in range(len(actual_pets_amount)):
        assert pet_names[i].text != ''
        assert pet_ages[i].text != ''
        assert pet_breeds[i].text != ''

def test_check_our_pets_names():
    # Проходим весь процесс авторизации и входа в свой аккаунт
    pytest.driver.find_element_by_id('email').send_keys('hjkhd667oo@hohoho.ya')
    pytest.driver.find_element_by_id('pass').send_keys('iuuklpiu777896Ty')
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    pytest.driver.find_element_by_link_text('Мои питомцы').click()
    assert pytest.driver.find_element_by_tag_name('h2').text == 'matyuin'
    # Повторяем переменную с именами своих питомцев
    pet_names = WebDriverWait(pytest.driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//td[1]')))
    # Пункт 4: У всех питомцев разные имена
    i = 0
    while i < len(pet_names):
        j = i + 1
        while j < len(pet_names):
            assert pet_names[i].text != pet_names[j].text
            j += 1
        i += 1

def test_if_some_pets_are_the_same():
    # Проходим весь процесс авторизации и входа в свой аккаунт
    pytest.driver.find_element_by_id('email').send_keys('hjkhd667oo@hohoho.ya')
    pytest.driver.find_element_by_id('pass').send_keys('iuuklpiu777896Ty')
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    pytest.driver.find_element_by_link_text('Мои питомцы').click()
    assert pytest.driver.find_element_by_tag_name('h2').text == 'matyuin'
    # Переменная с явным ожиданием, где хранятся имена, возраста и породы наших питомцев в таблице
    # В том числе и крестики для удаления питомцев
    pets_table = WebDriverWait(pytest.driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.table.table-hover td')))
    # Переменная, устанавливающая количество столбцов (имя, возраст, порода, крестик)
    j = 4
    # Избавляемся от крестика, так как он нам не нужен
    del pets_table[j - 1::j]
    # Пункт 5: В списке нет повторяющихся питомцев
    pet_list = []
    for pet in pets_table:
        pet = pet.text
        pet_list.append(pet)
    pet_list = tuple(pet_list)
    pets_check = tuple(pet_list[i:i + 3] for i in range(0, len(pet_list), 3))
    to_check_pets = set(pets_check)
    assert len(pets_check) == len(to_check_pets)



