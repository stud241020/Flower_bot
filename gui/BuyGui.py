from telebot import types


# Меню добавления в корзину
class BuyGUI:

    @staticmethod
    def get_buy_menu(prod_id, _quantity):
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        plus_data = int(_quantity) + 1
        minus_data = int(_quantity) - 1
        plus = types.InlineKeyboardButton(text="+", callback_data="Товар:" + str(prod_id) + ":" + str(plus_data))
        quantity = types.InlineKeyboardButton(text=str(_quantity), callback_data="quantity")
        minus = types.InlineKeyboardButton(text="-", callback_data="Товар:" + str(prod_id) + ":" + str(minus_data))
        add_to_cart = types.InlineKeyboardButton(text="Добавить в корзину", callback_data="add_to_cart:=" + str(prod_id)
                                                                                          + ":"
                                                                                          + str(_quantity)
                                                                                          + ";")
        keyboard.add(minus, quantity, plus)
        keyboard.add(add_to_cart)
        return keyboard
