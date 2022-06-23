import tools.CommandSystem as command_system
from tools.DatabaseModule import Database
from tools.CommandResult import CommandResult


# Разбираем сколько и каких товаров добавить в заказ
def parse_order(text):
    command, data = str(text).split("=", 2)
    products = data.split(";")
    _ids = []
    _quantities = []
    for product in products:
        if product != "":
            _id, _quantity = product.split(":")
            _ids.append(_id.strip(" "))
            _quantities.append(_quantity.strip(" "))
    return _ids, _quantities


# Добавляем в коризну
def add_to_cart(id, text):
    try:
        products, quantity = parse_order(text)
        db = Database()
        db.fill_user_cart(id, products, quantity)
        result = CommandResult("Все товары успешно добавлены в корзину", image=r"https://telegram-flowers.herokuapp.com"
                                                                               r"/files/success_add_to_cart.jpg")
        return result
    except:
        result = CommandResult("Произошла ошибка", image=r"https://telegram-flowers.herokuapp.com/files/"
                                                         r"error_add_to_cart.gif")
        return result


add_to_cart_command = command_system.Command()

add_to_cart_command.keys = ['add_to_cart']
add_to_cart_command.description = 'Добавление в корзину'
add_to_cart_command.process = add_to_cart
