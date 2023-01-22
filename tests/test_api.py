import os

import yaml
import requests

dir_path = os.path.dirname(os.path.realpath(__file__))

with open(f'{dir_path}/config.yaml', 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

LOCAL_PORT = os.environ.get('APP_PORT')
LOCAL_URL = f'http://localhost:{LOCAL_PORT}/api/v1/menus'


#1 Просматриваем список меню
def test_response_menu_get_list():
    response = requests.get(LOCAL_URL)
    assert response.status_code == 200

#2 Создаем новое меню
def test_response_menu_post():
    data = {
        "title": config['app']['target_menu_title'],
        "description": config['app']['target_menu_description']
    }
    response = requests.post(LOCAL_URL, json=data)
    config['app']['target_menu_id'] = response.json()['id']
    assert response.status_code == 201
    assert response.json()['title'] == config['app']['target_menu_title']
    assert response.json()['description'] == config['app']['target_menu_description']

#3 Просматриваем определенное меню
def test_response_get_target_menu():
    url = f"{LOCAL_URL}/{config['app']['target_menu_id']}"
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json()['id'] == config['app']['target_menu_id']
    assert response.json()['title'] == config['app']['target_menu_title']
    assert response.json()['description'] == config['app']['target_menu_description']

#4 Вносим изменения в определенное меню
def test_response_patch_target_menu():
    url = f"{LOCAL_URL}/{config['app']['target_menu_id']}"
    data = {
        "title": "My updated menu 1",
        "description": "My updated menu description 1"
    }
    response = requests.patch(url, json=data)
    assert response.status_code == 200
    assert response.json()['title'] != config['app']['target_menu_title']
    assert response.json()['description'] != config['app']['target_menu_description']


#5 Просматриваем список подменю
def test_response_submenu_get_list():
    url = f"{LOCAL_URL}/{config['app']['target_menu_id']}/submenus"
    response = requests.get(url)
    assert response.status_code == 200

#6 Проверяем создания нового подменю
def test_response_submenu_post():
    url = f"{LOCAL_URL}/{config['app']['target_menu_id']}/submenus"
    data = {
        "title": config['app']['target_submenu_title'],
        "description": config['app']['target_submenu_description']
    }
    response = requests.post(url, json=data)
    config['app']['target_submenu_id'] = response.json()['id']
    assert response.status_code == 201
    assert response.json()['title'] == config['app']['target_submenu_title']
    assert response.json()['description'] == config['app']['target_submenu_description']

#7 Просматриваем определенное подменю
def test_response_get_target_submenu():
    url = f"{LOCAL_URL}/{config['app']['target_menu_id']}/" \
          f"submenus/{config['app']['target_submenu_id']}"
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json()['id'] == config['app']['target_submenu_id']
    assert response.json()['title'] == config['app']['target_submenu_title']
    assert response.json()['description'] == config['app']['target_submenu_description']

#8 Вносим изменения в определенное подменю
def test_response_patch_target_submenu():
    url = f"{LOCAL_URL}/{config['app']['target_menu_id']}/" \
          f"submenus/{config['app']['target_submenu_id']}"
    data = {
        "title": "My updated submenu 1",
        "description": "My updated submenu description 1"
    }
    response = requests.patch(url, json=data)
    assert response.status_code == 200
    assert response.json()['title'] != config['app']['target_submenu_title']
    assert response.json()['description'] != config['app']['target_submenu_description']


#9 Просматриваем список блюд
def test_response_dish_get_list():
    url = f"{LOCAL_URL}/{config['app']['target_menu_id']}/" \
          f"submenus/{config['app']['target_submenu_id']}/dishes"
    response = requests.get(url)
    assert response.status_code == 200

#10 Проверяем создания нового блюда
def test_response_dish_post():
    url = f"{LOCAL_URL}/{config['app']['target_menu_id']}/" \
          f"submenus/{config['app']['target_submenu_id']}/dishes"
    data = {
        "title": config['app']['target_dish_title'],
        "description": config['app']['target_dish_description'],
        "price": "12.50"
    }
    response = requests.post(url, json=data)
    config['app']['target_dish_id'] = response.json()['id']
    assert response.status_code == 201
    assert response.json()['title'] == config['app']['target_dish_title']
    assert response.json()['description'] == config['app']['target_dish_description']

#11 Просматриваем определенное блюдо
def test_response_get_target_dish():
    url = f"{LOCAL_URL}/{config['app']['target_menu_id']}/" \
          f"submenus/{config['app']['target_submenu_id']}/dishes/" \
          f"{config['app']['target_dish_id']}"
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json()['id'] == config['app']['target_dish_id']
    assert response.json()['title'] == config['app']['target_dish_title']
    assert response.json()['description'] == config['app']['target_dish_description']

#12 Вносим изменения в определенное блюдо
def test_response_patch_target_dish():
    url = f"{LOCAL_URL}/{config['app']['target_menu_id']}/" \
          f"submenus/{config['app']['target_submenu_id']}/dishes/" \
          f"{config['app']['target_dish_id']}"
    data = {
        "title": "My updated dish 1",
        "description": "My updated dish description 1",
        "price": "17.90"
    }
    response = requests.patch(url, json=data)
    assert response.status_code == 200
    assert response.json()['title'] != config['app']['target_dish_title']
    assert response.json()['description'] != config['app']['target_dish_description']
    assert response.json()['price'] != config['app']['target_dish_price']

#13 Проверяем количество подменю и блюд в меню
def test_response_get_target_menu_count_submenus_and_dishes():
    url = f"{LOCAL_URL}/{config['app']['target_menu_id']}"
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json()['submenus_count'] == 1
    assert response.json()['dishes_count'] == 1

#14 Проверяем количество блюд в подменю
def test_response_get_target_submenu_count__dishes():
    url = f"{LOCAL_URL}/{config['app']['target_menu_id']}/" \
          f"submenus/{config['app']['target_submenu_id']}"
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json()['dishes_count'] == 1


# Удаляем блюдо
# def test_response_delete_target_dish():
#    url = f"{LOCAL_URL}/{config['app']['target_menu_id']}/" \
#          f"submenus/{config['app']['target_submenu_id']}/dishes/" \
#          f"{config['app']['target_dish_id']}"
#    response = requests.delete(url)
#    assert response.status_code == 200

#15 Удаляем подменю
def test_response_delete_target_submenu():
    url = f"{LOCAL_URL}/{config['app']['target_menu_id']}/" \
          f"submenus/{config['app']['target_submenu_id']}"
    response = requests.delete(url)
    assert response.status_code == 200

#16 Удаляем меню
def test_response_delete_target_menu():
    url = f"{LOCAL_URL}/{config['app']['target_menu_id']}"
    response = requests.delete(url)
    assert response.status_code == 200

#17 Проверяем, что список блюд пустой (проверка каскадного удаления)
def test_response_dish_get_list_is_empty():
    url = f"{LOCAL_URL}/{config['app']['target_menu_id']}/" \
          f"submenus/{config['app']['target_submenu_id']}/dishes"
    response = requests.get(url)
    assert response.json() == []

#

#

#

#
