import tools.CommandSystem as command_system
from tools.DatabaseModule import Database
from tools.CommandResult import CommandResult
from tools.WooCommerceAPI import WC_API
from tools.ProductsParser import ProductsParser
from gui.CartProductGui import CartProductGUI


# Вывести корзину
def parse_cart_data(id, data):
    _products = dict()
    products = []
    for item in data:
        _products[str(item[0])] = (_products.get(str(item[0])) or 0) + item[1]
    wc = WC_API()
    wc_products = wc.get_all_products()
    products_keys = list(_products.keys())
    for product in wc_products:
        if str(product['id']) in products_keys:
            product_id = product['id']
            product_image = product['images'][0]['src']
            product_data = "<b>Товар</b>" + ": " + product['name'] + "\n\n<b>Цена</b>: " + product['price'] + "руб. \n\n<i>" \
                           + ProductsParser.remove_html_from_text(product['description']) + "</i>"
            product_quantity = _products[str(product_id)]
            _product = CommandResult(text=product_data, image=product_image,
                                     menu=CartProductGUI.get_cart_gui(product_id, product_quantity, id))
            products.append(_product)
    return products


def show_cart(id, text):
    db = Database()
    data = db.get_user_cart_data(id)
    products = parse_cart_data(id, data)
    if len(products) > 0:
        return CommandResult("<pre>Ваша корзина: </pre>\n\n", custom_data=products)
    else:
        return CommandResult("<b>Ваша корзина пуста. Добавьте в неё товары и оформите заказ.</b>")


show_cart_command = command_system.Command()

show_cart_command.keys = ['\U0001F6D2 Корзина', 'Корзина', 'корзина', 'заказ']
show_cart_command.description = 'Показать корзину'
show_cart_command.process = show_cart
