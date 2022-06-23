import tools.CommandSystem as command_system
from tools.DatabaseModule import Database
from tools.CommandResult import CommandResult
from gui.CartProductGui import CartProductGUI

#Отвечает за + и - внизу товара
def set_product(id, text):
    command, product, quantity = text.split(":")
    if int(quantity) < 1:
        quantity = "1"
    db = Database()
    db.set_product_quantity(id, product, quantity)
    result = CommandResult("", menu=CartProductGUI.get_cart_gui(product, quantity, id))
    return result


set_product_command = command_system.Command()

set_product_command.keys = ['set_product']
set_product_command.description = 'Изменение количества товара в корзине'
set_product_command.process = set_product
