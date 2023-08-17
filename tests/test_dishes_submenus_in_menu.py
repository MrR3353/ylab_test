import test_dish
import test_menu
import test_submenu
from httpx import AsyncClient


async def test_add_menu_submenu_dishes(ac: AsyncClient) -> None:
    await test_menu.test_add_menu(ac)
    await test_submenu.test_add_submenu(ac)
    await test_dish.test_add_dish(ac)
    await test_dish.test_add_dish(ac)


async def test_get_menu(ac: AsyncClient) -> None:
    test_menu.LAST_MENU = (await ac.get(f'/api/v1/menus/{test_menu.LAST_MENU["id"]}')).json()
    await test_menu.test_get_menu(ac)
    assert 'id' in test_menu.LAST_MENU
    assert test_menu.LAST_MENU['submenus_count'] == 1
    assert test_menu.LAST_MENU['dishes_count'] == 2


async def test_get_submenu(ac: AsyncClient) -> None:
    test_submenu.LAST_SUBMENU = (await ac.get(f'/api/v1/menus/{test_menu.LAST_MENU["id"]}/submenus/{test_submenu.LAST_SUBMENU["id"]}')).json()
    await test_submenu.test_get_submenu(ac)
    assert 'id' in test_submenu.LAST_SUBMENU
    assert test_submenu.LAST_SUBMENU['dishes_count'] == 2


async def test_delete_submenu(ac: AsyncClient) -> None:
    await test_submenu.test_delete_submenu(ac, count=1)


async def test_get_all_submenu(ac: AsyncClient) -> None:
    response = await ac.get(f'/api/v1/menus/{test_menu.LAST_MENU["id"]}/submenus/')
    assert response.json() == []
    assert response.status_code == 200


async def test_get_all_dishes(ac: AsyncClient) -> None:
    response = await ac.get(f'/api/v1/menus/{test_menu.LAST_MENU["id"]}/submenus/{test_submenu.LAST_SUBMENU.get("id", 0)}/dishes/')
    assert response.json() == []
    assert response.status_code == 200


async def test_get_menu2(ac: AsyncClient) -> None:
    test_menu.LAST_MENU = (await ac.get(f'/api/v1/menus/{test_menu.LAST_MENU["id"]}')).json()
    await test_menu.test_get_menu(ac)
    assert test_menu.LAST_MENU['submenus_count'] == 0
    assert test_menu.LAST_MENU['dishes_count'] == 0


async def test_delete_menu(ac: AsyncClient) -> None:
    await test_menu.test_delete_menu(ac, 1)


async def test_get_all_menu(ac: AsyncClient) -> None:
    response = await ac.get('/api/v1/menus/')
    assert response.json() == []
    assert response.status_code == 200
