from telebot import types


# Класс, формирования меню
class GUI:

    # inline - menu (каталог)
    @staticmethod
    def get_inline_menu(data, callback_data):
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard_item_first = types.InlineKeyboardButton(text=data[0],
                                                         switch_inline_query_current_chat=callback_data[0], row_width=1)
        keyboard.add(keyboard_item_first)  #"Все категории"
        i = 1
        while i < (len(data) - 1):  #Две колонки с остальными категориями
            keyboard_item_first = types.InlineKeyboardButton(text=data[i],
                                                             switch_inline_query_current_chat=callback_data[i])
            keyboard_item_second = types.InlineKeyboardButton(text=data[i + 1],
                                                              switch_inline_query_current_chat=callback_data[i + 1])
            keyboard.add(keyboard_item_first, keyboard_item_second, row_width=2)
            i += 2
        if len(data) % 2 == 0: #если категорий четное кол-во, то последняя тоже широкая
            keyboard_item_first = types.InlineKeyboardButton(text=data[len(data) - 1],
                                                             switch_inline_query_current_chat=callback_data[len(data) - 1])
            keyboard.add(keyboard_item_first)
        return keyboard

    # Обычнон меню
    @staticmethod
    def get_menu(first_col, second_col, third_col):
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True) #создание клавиатуры
        first_0 = GUI.form_keyboard_button(first_col[0]) #формирование кнопок
        first_1 = GUI.form_keyboard_button(first_col[1])
        second_0 = GUI.form_keyboard_button(second_col[0])
        second_1 = GUI.form_keyboard_button(second_col[1])
        third = GUI.form_keyboard_button(third_col)
        keyboard.add(first_0, first_1)
        keyboard.add(second_0, second_1)
        keyboard.add(third)
        return keyboard

    @staticmethod
    def form_keyboard_button(item):
        webapp = types.WebAppInfo("https://telegram-flowers.herokuapp.com")
        if item == u"\U0001F5A5 Web-приложение":
            keyboard_item = types.KeyboardButton(item, web_app=webapp)
        else:
            keyboard_item = types.KeyboardButton(item)
        return keyboard_item


