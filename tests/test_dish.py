from httpx import AsyncClient
import test_menu, test_submenu

LAST_DISH = {}


async def test_add_menu_submenu(ac: AsyncClient):
    await test_menu.test_add_menu(ac)
    await test_submenu.test_add_submenu(ac)


async def test_add_dish(ac: AsyncClient):
    global LAST_DISH
    new_dish = {
        "title": "Submenu title 1",
        "description": "Submenu description 1",
        "price": "18.23"
    }
    response = await ac.post(f'/api/v1/menus/{test_menu.LAST_MENU["id"]}/submenus/{test_submenu.LAST_SUBMENU["id"]}/dishes/', json=new_dish)
    LAST_DISH = response.json()
    assert LAST_DISH['title'] == new_dish['title']
    assert LAST_DISH['description'] == new_dish['description']
    assert response.status_code == 201


async def test_get_dish(ac: AsyncClient):
    response = await ac.get(f'/api/v1/menus/{test_menu.LAST_MENU["id"]}/submenus/{test_submenu.LAST_SUBMENU["id"]}/dishes/{LAST_DISH["id"]}')
    assert response.json() == LAST_DISH
    assert response.status_code == 200


async def test_update_dish(ac: AsyncClient):
    global LAST_DISH
    new_dish = {
        "title": "Updated dish title 1",
        "description": "Updated dish description 1",
        "price": "19.10"
    }
    response = await ac.patch(f'/api/v1/menus/{test_menu.LAST_MENU["id"]}/submenus/{test_submenu.LAST_SUBMENU["id"]}/dishes/{LAST_DISH["id"]}', json=new_dish)
    LAST_DISH = response.json()
    assert LAST_DISH['title'] == new_dish['title']
    assert LAST_DISH['description'] == new_dish['description']
    assert response.status_code == 200


async def test_get_all_dishes(ac: AsyncClient):
    response = await ac.get(f'/api/v1/menus/{test_menu.LAST_MENU["id"]}/submenus/{test_submenu.LAST_SUBMENU["id"]}/dishes/')
    assert response.json() == [LAST_DISH]
    assert response.status_code == 200


async def test_get_all_dishes2(ac: AsyncClient):
    # adding 2nd dish
    await test_add_dish(ac)
    response = await ac.get(f'/api/v1/menus/{test_menu.LAST_MENU["id"]}/submenus/{test_submenu.LAST_SUBMENU["id"]}/dishes/')
    assert len(response.json()) == 2
    assert response.status_code == 200


async def test_delete_dishes(ac: AsyncClient, count=2):
    global LAST_DISH
    # deleting 2 dishes by default
    for i in range(count):
        get_all_response = await ac.get(f'/api/v1/menus/{test_menu.LAST_MENU["id"]}/submenus/{test_submenu.LAST_SUBMENU["id"]}/dishes/')
        get_all_response = get_all_response.json()[:-1]

        response = await ac.delete(f'/api/v1/menus/{test_menu.LAST_MENU["id"]}/submenus/{test_submenu.LAST_SUBMENU["id"]}/dishes/{LAST_DISH["id"]}')
        assert response.status_code == 200
        response = await ac.get(f'/api/v1/menus/{test_menu.LAST_MENU["id"]}/submenus/{test_submenu.LAST_SUBMENU["id"]}/dishes/')
        LAST_DISH = get_all_response[-1] if get_all_response else {}
        assert get_all_response == response.json()
        assert response.status_code == 200


async def test_delete_menu(ac: AsyncClient):
    await test_menu.test_delete_menu(ac, count=1)
