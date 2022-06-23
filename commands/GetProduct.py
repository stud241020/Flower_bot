import tools.CommandSystem as command_system
from tools.WooCommerceAPI import WC_API
from tools.ProductsParser import ProductsParser
from tools.CommandResult import CommandResult
from gui.BuyGui import BuyGUI


# Получить конкретный продукт
def get_product(id, text):
    wc_data = WC_API()
    label, prod_id, quantity = text.split(":", 3)
    if int(quantity) < 1:
        quantity = "1"
    product = wc_data.get_product_by_id(prod_id.strip())
    product_image = product['images'][0]['src']
    product_data = "<b>" + label + "</b>" + ": " + product['name'] + "\n\n<b>Цена</b>: " + product['price'] + "руб. \n\n<i>" + ProductsParser.remove_html_from_text(product['description']) + "</i>"
    result = CommandResult(text=product_data, image=product_image, menu=BuyGUI.get_buy_menu(prod_id, quantity))
    return result


get_product_command = command_system.Command()

get_product_command.keys = ['Товар', 'товар']
get_product_command.description = 'Вывод товара'
get_product_command.process = get_product

