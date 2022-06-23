from telebot import types

#+-убрать из корзины
class CartProductGUI:

    @staticmethod
    def get_cart_gui(product, _quantity, user):
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        plus_data = int(_quantity) + 1
        minus_data = int(_quantity) - 1
        plus = types.InlineKeyboardButton(text="+", callback_data="set_product:" + str(product) + ":" + str(plus_data))
        quantity = types.InlineKeyboardButton(text=str(_quantity), callback_data="quantity")
        minus = types.InlineKeyboardButton(text="-", callback_data="set_product:" + str(product) + ":" + str(minus_data))
        add_to_cart = types.InlineKeyboardButton(text="Убрать из корзины", callback_data="remove_all_from_cart:"
                                                                                         + str(product))
        keyboard.add(minus, quantity, plus)
        keyboard.add(add_to_cart)
        return keyboard
