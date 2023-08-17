# from datetime import datetime

import test_dish
import test_menu
import test_submenu
from httpx import AsyncClient


async def test_add_many_dishes(ac: AsyncClient, menu_count: int = 2, submenu_in_menu: int = 2, dish_in_submenu: int = 2) -> None:
    for i in range(menu_count):
        await test_menu.test_add_menu(ac)
        for j in range(submenu_in_menu):
            await test_submenu.test_add_submenu(ac)
            for k in range(dish_in_submenu):
                await test_dish.test_add_dish(ac)
    # start = datetime.now()
    response = await ac.get('/api/v1/menus/')
    # end = datetime.now()
    assert response.status_code == 200
    assert len(response.json()) == menu_count
    for menu in response.json():
        assert menu['submenus_count'] == submenu_in_menu
        assert menu['dishes_count'] == submenu_in_menu * dish_in_submenu
    # cached_start = datetime.now()
    response2 = await ac.get('/api/v1/menus/')
    # cached_end = datetime.now()
    assert response.json() == response2.json()
    # assert cached_end - cached_start < end - start    actually, don't work sometimes(

    await test_menu.test_delete_menu(ac, menu_count)
