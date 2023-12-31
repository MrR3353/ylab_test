import test_menu
import test_submenu
from httpx import AsyncClient

LAST_DISH = {}


async def test_add_menu_submenu(ac: AsyncClient) -> None:
    await test_menu.test_add_menu(ac)
    await test_submenu.test_add_submenu(ac)


async def test_add_dish(ac: AsyncClient) -> None:
    global LAST_DISH
    new_dish = {
        'title': 'Submenu title 1',
        'description': 'Submenu description 1',
        'price': '18.23'
    }
    response = await ac.post(f'/api/v1/menus/{test_menu.LAST_MENU["id"]}/submenus/{test_submenu.LAST_SUBMENU["id"]}/dishes/', json=new_dish)
    LAST_DISH = response.json()
    assert LAST_DISH['title'] == new_dish['title']
    assert LAST_DISH['description'] == new_dish['description']
    assert response.status_code == 201
    test_submenu.LAST_SUBMENU['dishes_count'] += 1
    test_menu.LAST_MENU['dishes_count'] += 1


async def test_get_dish(ac: AsyncClient) -> None:
    response = await ac.get(f'/api/v1/menus/{test_menu.LAST_MENU["id"]}/submenus/{test_submenu.LAST_SUBMENU["id"]}/dishes/{LAST_DISH["id"]}')
    assert response.json() == LAST_DISH
    assert response.status_code == 200


async def test_update_dish(ac: AsyncClient) -> None:
    global LAST_DISH
    new_dish = {
        'title': 'Updated dish title 1',
        'description': 'Updated dish description 1',
        'price': '19.10'
    }
    response = await ac.patch(f'/api/v1/menus/{test_menu.LAST_MENU["id"]}/submenus/{test_submenu.LAST_SUBMENU["id"]}/dishes/{LAST_DISH["id"]}', json=new_dish)
    LAST_DISH = response.json()
    assert LAST_DISH['title'] == new_dish['title']
    assert LAST_DISH['description'] == new_dish['description']
    assert response.status_code == 200


async def test_get_all_dishes(ac: AsyncClient) -> None:
    response = await ac.get(f'/api/v1/menus/{test_menu.LAST_MENU["id"]}/submenus/{test_submenu.LAST_SUBMENU["id"]}/dishes/')
    assert response.json() == [LAST_DISH]
    assert response.status_code == 200


async def test_get_all_dishes2(ac: AsyncClient) -> None:
    # adding 2nd dish
    await test_add_dish(ac)
    response = await ac.get(f'/api/v1/menus/{test_menu.LAST_MENU["id"]}/submenus/{test_submenu.LAST_SUBMENU["id"]}/dishes/')
    assert len(response.json()) == 2
    assert response.status_code == 200


async def test_delete_dishes(ac: AsyncClient, count: int = 2) -> None:
    global LAST_DISH
    # deleting 2 dishes by default
    for i in range(count):
        get_all_response = await ac.get(f'/api/v1/menus/{test_menu.LAST_MENU["id"]}/submenus/{test_submenu.LAST_SUBMENU["id"]}/dishes/')
        get_all_response = get_all_response.json()
        get_all_response.remove(LAST_DISH)

        response = await ac.delete(f'/api/v1/menus/{test_menu.LAST_MENU["id"]}/submenus/{test_submenu.LAST_SUBMENU["id"]}/dishes/{LAST_DISH["id"]}')
        assert response.status_code == 200
        response = await ac.get(f'/api/v1/menus/{test_menu.LAST_MENU["id"]}/submenus/{test_submenu.LAST_SUBMENU["id"]}/dishes/')
        LAST_DISH = get_all_response[-1] if get_all_response else {}
        assert get_all_response == response.json()
        assert response.status_code == 200
        test_submenu.LAST_SUBMENU['dishes_count'] -= 1
        test_menu.LAST_MENU['dishes_count'] -= 1


async def test_delete_menu(ac: AsyncClient) -> None:
    await test_menu.test_delete_menu(ac, count=1)
