from httpx import AsyncClient

LAST_MENU = {}


async def test_add_menu(ac: AsyncClient):
    global LAST_MENU
    new_menu = {
        'title': 'Test title 1',
        'description': 'test description 1'
    }
    response = await ac.post('/api/v1/menus/', json=new_menu)
    LAST_MENU = response.json()
    assert LAST_MENU['title'] == new_menu['title']
    assert LAST_MENU['description'] == new_menu['description']
    assert response.status_code == 201


async def test_get_menu(ac: AsyncClient):
    response = await ac.get(f'/api/v1/menus/{LAST_MENU["id"]}')
    assert response.json() == LAST_MENU
    assert response.status_code == 200


async def test_update_menu(ac: AsyncClient):
    global LAST_MENU
    new_menu = {
        'title': 'Updated title 1',
        'description': 'Updated description 1'
    }
    response = await ac.patch(f'/api/v1/menus/{LAST_MENU["id"]}', json=new_menu)
    LAST_MENU = response.json()
    assert LAST_MENU['title'] == new_menu['title']
    assert LAST_MENU['description'] == new_menu['description']
    assert response.status_code == 200


async def test_get_all_menu(ac: AsyncClient):
    response = await ac.get('/api/v1/menus/')
    assert response.json() == [LAST_MENU]
    assert response.status_code == 200


async def test_get_all_menu2(ac: AsyncClient):
    # adding 2nd menu
    await test_add_menu(ac)
    response = await ac.get('/api/v1/menus/')
    assert len(response.json()) == 2
    assert response.status_code == 200


async def test_delete_menu(ac: AsyncClient, count=2):
    global LAST_MENU
    # deleting 2 menus by default
    for i in range(count):
        get_all_response = await ac.get('/api/v1/menus/')
        get_all_response = get_all_response.json()
        get_all_response.remove(LAST_MENU)

        response = await ac.delete(f'/api/v1/menus/{LAST_MENU["id"]}')
        assert response.status_code == 200
        response = await ac.get('/api/v1/menus/')
        LAST_MENU = get_all_response[-1] if get_all_response else {}
        assert get_all_response == response.json()
        assert response.status_code == 200
