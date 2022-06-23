from gui.AbstractGui import GUI


# Главное меню
class MainGUI:

    @staticmethod
    def get_main_menu():
        first_column = [u'\U0001F3EA Каталог', u'\U0001F6D2 Корзина', ]
        second_column = [u'\U0001F33C Распознавание цветов',
                         u'\U00002139 О нас']
        third_row = u"\U0001F5A5 Web-приложение"
        return GUI.get_menu(first_column, second_column, third_row)
