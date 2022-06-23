import tools.CommandSystem as command_system
from tools.WooCommerceAPI import WC_API
from telebot import types
from tools.CommandResult import CommandResult
from tools.ProductsParser import ProductsParser


# Получить продукты по категориям
def get_category_products(id, text):
    if str(text).startswith("@"):
        text = text.replace("@", "")
        wc_data = WC_API()
        data = wc_data.get_all_products()
        answer = []
        for i in range(0, len(data)):
            for j in range(0, len(data[i]['categories'])):
                if data[i]['categories'][j]['name'].lower() == text.lower():
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
                             "<i>@flowers_shop_bryansk_bot {0}</i>\n\n"
                             "<b>Или используйте встроенное меню и команду <u>Каталог</u></b>".format(text))


get_category_products_command = command_system.Command()

wc = WC_API()
keys = [x.lower() for x in ProductsParser.get_categories_names(wc.get_categories())]

get_category_products_command.keys = keys
get_category_products_command.description = 'Вывод списка товаров определенной категории'
get_category_products_command.process = get_category_products
