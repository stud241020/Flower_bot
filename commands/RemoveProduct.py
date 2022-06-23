import tools.CommandSystem as command_system
from tools.DatabaseModule import Database
from tools.CommandResult import CommandResult



def remove_product(id, text):
    command, product = text.split(":")
    db = Database()
    db.remove_product_from_cart(id, product)
    result = CommandResult("Товар удалён")
    return result


remove_product_command = command_system.Command()

remove_product_command.keys = ['remove_all_from_cart']
remove_product_command.description = 'Удаление товара из корзины'
remove_product_command.process = remove_product
