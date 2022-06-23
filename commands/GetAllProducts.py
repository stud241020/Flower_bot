import tools.CommandSystem as command_system
from tools.WooCommerceAPI import WC_API
from telebot import types
from tools.CommandResult import CommandResult


# Получить все продукты
def get_all_products(id, text):
    if str(text).startswith("@"):

        wc_data = WC_API()
        data = wc_data.get_all_products()
        answer = []
        for i in range(0, len(data)):
            answer.append(types.InlineQueryResultArticle(id=i+1, title=data[i]['name'],
                                                    description=data[i]['price'] + " руб.",
                                                    input_message_content=
                                                    types.InputTextMessageContent(message_text="Товар: " + str(data[i]['id']) + ":1"),
                                                    thumb_url=data[i]['images'][0]['src'],
                                                    thumb_width=48, thumb_height=48))
        result = CommandResult(menu=answer)
        return result
    else:
        return CommandResult("<pre>Чтобы посмотреть товары бота используйте команду:</pre>\n\n"
                             "<i>@flowers_shop_bryansk_bot Товары</i>\n\n"
                             "<b>Или используйте встроенное меню и команду <u>Каталог</u></b>")


get_products_command = command_system.Command()

get_products_command.keys = ['Товары', 'товары']
get_products_command.description = 'Вывод списка товаров'
get_products_command.process = get_all_products
