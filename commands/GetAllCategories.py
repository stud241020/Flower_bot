import tools.CommandSystem as command_system
from tools.WooCommerceAPI import WC_API
from telebot import types
from gui.CategoriesMenu import CategoriesGUI
from tools.CommandResult import CommandResult


# Получить все категории
def get_all_categories(id, text):
    wc_data = WC_API()
    data = wc_data.get_categories()
    categories_gui = CategoriesGUI.get_categories_menu(data)
    result = CommandResult("Выберите категорию", menu=categories_gui)
    return result


get_categories_command = command_system.Command()

get_categories_command.keys = ['Магазин', 'Каталог', u'\U0001F3EA Каталог']
get_categories_command.description = 'Вывод списка товаров'
get_categories_command.process = get_all_categories
