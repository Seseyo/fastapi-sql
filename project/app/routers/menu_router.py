from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from db.config import session

from db.models.menu import Menu
from db.models.submenu import Submenu
from db.models.dish import Dish

router = APIRouter()

# Обработка запросов CRUD для Меню

# Просматривает список меню
@router.get("/api/v1/menus")
def get_menus():
    menus = session.query(Menu).all()
    return menus

# Создаем новое меню
@router.post("/api/v1/menus", status_code=201)
def create_menu(data=Body()):
    new_menu = Menu(title=data["title"], description=data["description"])
    session.add(new_menu)
    session.commit()
    return {"id": str(new_menu.id), "title": new_menu.title,
            "description": new_menu.description}

# Просматривает определенное меню
@router.get("/api/v1/menus/{menu_id}")
def get_menu_by_id(menu_id):
    target_menu = session.get(Menu, menu_id)
    if target_menu != None:
        submenus = session.query(Submenu.id)
        submenus = submenus.filter(Submenu.menu_id==menu_id).all()
        dishes_count = 0
        for sub in submenus:
            q = session.query(Dish)
            q = q.filter(Dish.submenu_id==sub.id).count()
            dishes_count += q
        return {"id": str(target_menu.id), "title": target_menu.title,
                "description": target_menu.description,
                "submenus_count": len(submenus),
                "dishes_count": dishes_count}
    else:
        return JSONResponse(content={"detail": "menu not found"},
                            status_code=404)

# Обновляет меню
@router.patch("/api/v1/menus/{id}", status_code=200)
def update_menu(id, data=Body()):
    target_menu = session.get(Menu, id)
    target_menu.title = data['title']
    target_menu.description = data['description']
    session.commit()
    return {"id": str(target_menu.id), "title": target_menu.title,
            "description": target_menu.description}

# Удаляет меню
@router.delete("/api/v1/menus/{id}")
def delete_menu(id):
    target_menu = session.get(Menu, id)
    if target_menu != None:
        session.delete(target_menu)
        session.commit()
    return {"status": "true", "message": "The menu has been deleted"}

# Обработка запросов CRUD для Подменю

# Просматривает список подменю
@router.get("/api/v1/menus/{menu_id}/submenus")
def get_submenus(menu_id):
    submenus = session.query(Submenu)
    submenus = submenus.filter(Submenu.menu_id==menu_id).all()
    return submenus

# Создаем новое подменю
@router.post("/api/v1/menus/{menu_id}/submenus", status_code=201)
def create_submenu(menu_id, data=Body()):
    new_submenu = Submenu(title=data["title"],
                             description=data["description"],
                             menu_id=menu_id)
    session.add(new_submenu)
    session.commit()
    return {"id": str(new_submenu.id), "title": new_submenu.title,
            "description": new_submenu.description}

# Просматривает определенное подменю
@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def get_submenu_by_id(menu_id, submenu_id):
    target_submenu = session.query(Submenu)
    target_submenu = target_submenu.filter(Submenu.menu_id==menu_id)
    target_submenu = target_submenu.filter(Submenu.id==submenu_id).first()
    if target_submenu != None:
        dishes_count = session.query(Dish)
        dishes_count = dishes_count.filter(Dish.submenu_id==submenu_id)
        dishes_count = dishes_count.count()
        return {"id": str(target_submenu.id), "title": target_submenu.title,
                "description": target_submenu.description,
                "dishes_count": dishes_count}
    else:
        return JSONResponse(content={"detail": "submenu not found"},
                            status_code=404)

# Обновляет подменю
@router.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}", status_code=200)
def update_submenu(menu_id, submenu_id, data=Body()):
    target_submenu = session.query(Submenu)
    target_submenu = target_submenu.filter(Submenu.menu_id==menu_id)
    target_submenu = target_submenu.filter(Submenu.id==submenu_id).first()
    target_submenu.title = data['title']
    target_submenu.description = data['description']
    session.commit()
    return {"id": str(target_submenu.id), "title": target_submenu.title,
            "description": target_submenu.description}

# Удаляет подменю
@router.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def delete_submenu(menu_id, submenu_id):
    target_submenu = session.query(Submenu)
    target_submenu = target_submenu.filter(Submenu.menu_id==menu_id)
    target_submenu = target_submenu.filter(Submenu.id==submenu_id).first()
    if target_submenu != None:
        session.delete(target_submenu)
        session.commit()
    return {"status": "true", "message": "The submenu has been deleted"}


# Обработка запросов CRUD для Блюд

# Просматривает список блюд
@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
def get_dishes(menu_id, submenu_id):
    dishes = session.query(Dish).filter(Dish.submenu_id==submenu_id).all()
    return dishes

# Создаем новое блюдо
@router.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
          status_code=201)
def create_dish(menu_id, submenu_id, data=Body()):
    new_dish = Dish(title=data["title"], description=data["description"],
                       price=float(data["price"]), submenu_id=submenu_id)
    session.add(new_dish)
    session.commit()
    return {"id": str(new_dish.id), "title": new_dish.title,
            "description": new_dish.description,
            "price": '{:.2f}'.format(new_dish.price)}

# Просматривает определенное блюдо
@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def get_dish_by_id(menu_id, submenu_id, dish_id):
    target_dish = session.query(Dish)
    target_dish = target_dish.filter(Dish.submenu_id==submenu_id)
    target_dish = target_dish.filter(Dish.id==dish_id).first()
    if target_dish != None:
        return {"id": str(target_dish.id), "title": target_dish.title,
                "description": target_dish.description,
                "price": '{:.2f}'.format(target_dish.price)}
    else:
        return JSONResponse(content={"detail": "dish not found"},
                            status_code=404)

# Обновляет блюдо
@router.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
           status_code=200)
def update_dish(menu_id, submenu_id, dish_id, data=Body()):
    target_dish = session.query(Dish)
    target_dish = target_dish.filter(Dish.submenu_id==submenu_id)
    target_dish = target_dish.filter(Dish.id==dish_id).first()
    target_dish.title = data['title']
    target_dish.description = data['description']
    target_dish.price = float(data["price"])
    session.commit()
    return {"id": str(target_dish.id), "title": target_dish.title,
            "description": target_dish.description, "price": data["price"]}

# Удаляет блюдо
@router.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def delete_submenu(menu_id, submenu_id, dish_id):
    target_dish = session.query(Dish)
    target_dish = target_dish.filter(Dish.submenu_id==submenu_id)
    target_dish = target_dish.filter(Dish.id==dish_id).first()
    if target_dish != None:
        session.delete(target_dish)
        session.commit()
    return {  "status": "true", "message": "The dish has been deleted"}

#

#

#
