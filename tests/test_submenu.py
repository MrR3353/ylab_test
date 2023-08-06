import test_menu
from httpx import AsyncClient

LAST_SUBMENU = {}


async def test_add_menu(ac: AsyncClient):
    await test_menu.test_add_menu(ac)


async def test_add_submenu(ac: AsyncClient):
    global LAST_SUBMENU
    new_submenu = {
        'title': 'Submenu title 1',
        'description': 'Submenu description 1'
    }
    response = await ac.post(f'/api/v1/menus/{test_menu.LAST_MENU["id"]}/submenus/', json=new_submenu)
    LAST_SUBMENU = response.json()
    assert LAST_SUBMENU['title'] == new_submenu['title']
    assert LAST_SUBMENU['description'] == new_submenu['description']
    assert response.status_code == 201
    test_menu.LAST_MENU['submenus_count'] += 1


async def test_get_submenu(ac: AsyncClient):
    response = await ac.get(f'/api/v1/menus/{test_menu.LAST_MENU["id"]}/submenus/{LAST_SUBMENU["id"]}')
    assert response.json() == LAST_SUBMENU
    assert response.status_code == 200


async def test_update_submenu(ac: AsyncClient):
    global LAST_SUBMENU
    new_submenu = {
        'title': 'Updated submenu title 1',
        'description': 'Updated submenu description 1'
    }
    response = await ac.patch(f'/api/v1/menus/{test_menu.LAST_MENU["id"]}/submenus/{LAST_SUBMENU["id"]}', json=new_submenu)
    LAST_SUBMENU = response.json()
    assert LAST_SUBMENU['title'] == new_submenu['title']
    assert LAST_SUBMENU['description'] == new_submenu['description']
    assert response.status_code == 200


async def test_get_all_submenu(ac: AsyncClient):
    response = await ac.get(f'/api/v1/menus/{test_menu.LAST_MENU["id"]}/submenus/')
    assert response.json() == [LAST_SUBMENU]
    assert response.status_code == 200


async def test_get_all_submenu2(ac: AsyncClient):
    # adding 2nd submenu
    await test_add_submenu(ac)
    response = await ac.get(f'/api/v1/menus/{test_menu.LAST_MENU["id"]}/submenus/')
    assert len(response.json()) == 2
    assert response.status_code == 200


async def test_delete_submenu(ac: AsyncClient, count=2):
    global LAST_SUBMENU
    # deleting 2 submenus by default
    for i in range(count):
        get_all_response = await ac.get(f'/api/v1/menus/{test_menu.LAST_MENU["id"]}/submenus/')
        get_all_response = get_all_response.json()
        get_all_response.remove(LAST_SUBMENU)

        response = await ac.delete(f'/api/v1/menus/{test_menu.LAST_MENU["id"]}/submenus/{LAST_SUBMENU["id"]}')
        assert response.status_code == 200
        response = await ac.get(f'/api/v1/menus/{test_menu.LAST_MENU["id"]}/submenus/')
        LAST_SUBMENU = get_all_response[-1] if get_all_response else {}
        assert get_all_response == response.json()
        assert response.status_code == 200
        test_menu.LAST_MENU['submenus_count'] -= 1


async def test_delete_menu(ac: AsyncClient):
    await test_menu.test_delete_menu(ac, count=1)
