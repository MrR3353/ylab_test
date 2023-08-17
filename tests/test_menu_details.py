import test_dish
import test_menu
import test_submenu
from httpx import AsyncClient


async def test_menu_details(ac: AsyncClient, menu_count: int = 2, submenu_in_menu: int = 3, dish_in_submenu: int = 3) -> None:
    correct_menu = []
    for i in range(menu_count):
        await test_menu.test_add_menu(ac)
        menu_copy = test_menu.LAST_MENU.copy()  # don't change original menu
        menu_copy['submenus'] = []
        for j in range(submenu_in_menu):
            await test_submenu.test_add_submenu(ac)
            test_submenu.LAST_SUBMENU['dishes'] = []
            menu_copy['submenus'].append(test_submenu.LAST_SUBMENU)
            for k in range(dish_in_submenu):
                await test_dish.test_add_dish(ac)
                test_submenu.LAST_SUBMENU['dishes'].append(test_dish.LAST_DISH)
            del test_submenu.LAST_SUBMENU['dishes_count']
        del menu_copy['submenus_count']  # delete extra fields
        del menu_copy['dishes_count']
        correct_menu.append(menu_copy)

    response = await ac.get('/api/v1/menus/details')
    assert response.status_code == 200
    assert correct_menu == response.json()
    await test_menu.test_delete_menu(ac, count=menu_count)
