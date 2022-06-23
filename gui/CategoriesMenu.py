from gui.AbstractGui import GUI
from tools.ProductsParser import ProductsParser


# Меню категорий
class CategoriesGUI:

    @staticmethod
    def get_categories_menu(categories):
        data = ProductsParser.get_categories_names(categories)
        data.insert(0, "Все категории")
        callback_data = ProductsParser.get_categories_names(categories)
        callback_data.insert(0, "Товары")
        return GUI.get_inline_menu(data, callback_data)
