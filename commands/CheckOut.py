import tools.CommandSystem as command_system
from tools.DatabaseModule import Database
from tools.CommandResult import CommandResult
from tools.WooCommerceAPI import WC_API
from telebot import types


# Разбираем данные о заказа
def parse_order_data(data):
    _products = dict()
    products = []
    for item in data:
        _products[str(item[0])] = (_products.get(str(item[0])) or 0) + item[1]
    wc = WC_API()
    wc_products = wc.get_all_products()
    products_keys = list(_products.keys())
    for product in wc_products:
        if str(product['id']) in products_keys:
            products.append(types.LabeledPrice(label=product['name'], amount=int(product['price']) * 100 *
                                                                             int(_products[str(product['id'])])))
    return products, _products


# Сообщение об оплате для пользователя по айди из телеграма
def checkout(id, text):
    db = Database()
    data = db.get_user_cart_data(id)
    products, _products = parse_order_data(data)
    return CommandResult("Заказ для " + str(id), custom_data=products, products=_products)


checkout_command = command_system.Command()

checkout_command.keys = ['checkout']
checkout_command.description = 'Оформление заказа'
checkout_command.process = checkout
