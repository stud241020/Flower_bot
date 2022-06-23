import telebot
import os
import importlib
from tools.CommandSystem import command_list, command_list_keys
from tools.NatashaTextProcessing import NatashaProcessing
from telebot import types
from tools.WooCommerceAPI import WC_API
from tools.DatabaseModule import Database
import re


phone_number = re.compile("((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}")
bot = telebot.TeleBot('5103031753:AAG3NVWdGhPp16SdIA7u0o6fp-mG1tbhc2Y')  # Инициализируем бота токеном,
                                                                         # выданным @BotFather
provider_token = "401643678:TEST:da529bb5-30cf-4c0e-9d3b-081e68118fd7"  # Токен для оплаты, выдает @BotFather
cart_tags = ['\U0001F6D2 Корзина', 'Корзина', 'корзина', 'заказ']  # Команды корзины
cancel_tokens = ['отмена']


# Функция для генерации ответа по именам, названиям и т.п.
def get_fact_answer(text):
    return NatashaProcessing.get_fact_answer(text)


# Функция, проверяющая команды по нормальной форме слова
def get_unknown_command_result(text):
    return NatashaProcessing.find_command(text, command_list_keys)


# Поиск и выполнение команды
def execute_command(id, data, body):
    for c in command_list:
        if body in c.keys:
            reply = c.process(id, data)
            return reply
    return None


# Для команд вида callback
def get_callback_command_result(data):
    body = data.data.lower()
    body = body.split(":")[0]
    reply = execute_command(data.from_user.id, data.data, body)
    if reply is None:
        res = get_unknown_command_result(data.data)
        reply = execute_command(data.from_user.id, data.data, res)
    return reply


# Для команд из обычных сообщений
def get_command_result(data):
    body = data.text.lower()
    body = body.split(":")[0]
    reply = execute_command(data.from_user.id, data.text, body)
    if reply is None:  # Если команда не распознана, запускаем Natasha и ищем команду по нормальной форме слова
        res = get_unknown_command_result(data.text)
        reply = execute_command(data.from_user.id, data.text, res)
        if reply is None:  # Если команда все равно не найдена, запускаем Natasha для формирования ответа
            reply = get_fact_answer(data.text)
    return reply


def get_custom_result(data, text, command):
    body = command
    reply = execute_command(data.from_user.id, text, body)
    if reply is None:  # Если команда не распознана, запускаем Natasha и ищем команду по нормальной форме слова
        res = get_unknown_command_result(text)
        reply = execute_command(data.from_user.id, text, res)
        if reply is None:  # Если команда все равно не найдена, запускаем Natasha для формирования ответа
            reply = get_fact_answer(text)
    return reply


# Для оплаты
def get_checkout_result(data, text):
    body = "checkout"
    return get_custom_result(data, text, body)


# Для команд из веб-приложения
def get_web_app_command_result(data):
    body = data.web_app_data.data.lower()
    body = body.split(":")[0]
    reply = execute_command(data.from_user.id, data.web_app_data.data, body)
    return reply


# Для inline-команд
def get_inline_command_result(data):
    body = data.query.lower()
    reply = execute_command(data.from_user.id, "@" + data.query, body)
    if reply is None:  # Если команда не распознана, запускаем Natasha и ищем команду по нормальной форме слова
        res = get_unknown_command_result(data.query)
        reply = execute_command(data.from_user.id, data.query, res)
    return reply


# Функция, автоматически подключающая модули из папки commands
def load_modules():
    files = os.listdir(os.getcwd() + "/commands")
    modules = filter(lambda x: x.endswith('.py'), files)
    for m in modules:
        importlib.import_module("commands." + m[0:-3])


# Обработчик, команд из web-приложения
@bot.message_handler(content_types=['web_app_data'])
def web_app_data_handler(message):
    answer = get_web_app_command_result(message)
    bot.send_photo(message.from_user.id, answer.image, answer.text, parse_mode='HTML')


# Следующие 3 функции это последовательность при переходе в коризну
# Ввод телефона и выставление счёта
def input_user_phone(message, name, address):
    if message.text.lower() not in cancel_tokens:
        if phone_number.fullmatch(message.text.lower()):
            answer = get_checkout_result(message, message.text + ":" + address)
            wc = WC_API()
            invoice_payload = wc.make_order(message.from_user.id, answer.products, name, address, message.text)
            bot.send_invoice(message.from_user.id, "Заказ из \"цветочного мира\"", answer.text, invoice_payload,
                             provider_token, 'rub',
                             answer.custom_data, photo_url=r"https://telegram-flowers.herokuapp.com/files/order.png",
                             photo_height=224, photo_width=224, photo_size=224, is_flexible=False,
                             start_parameter='flowers_order')
        else:
            bot.send_message(message.from_user.id, "<b>Введите корректный номер телефона:</b>", parse_mode='HTML')
            bot.register_next_step_handler(message, input_user_phone, name, address)


# Ввод адресса
def input_user_address(message, name):
    if message.text.lower() not in cancel_tokens:
        bot.send_message(message.from_user.id, "<pre>Для отмены оформления заказа введите \"Отмена\"</pre>\n\n"
                                               "Введите свой номер телефона:", parse_mode='HTML')
        bot.register_next_step_handler(message, input_user_phone, name, message.text)


def input_user_name(message):
    if message.text.lower() not in cancel_tokens:
        bot.send_message(message.from_user.id, "<pre>Для отмены оформления заказа введите \"Отмена\"</pre>\n\n"
                                               "Введите адрес доставки:", parse_mode='HTML')
        bot.register_next_step_handler(message, input_user_address, message.text)


# Обработчик команды корзины
@bot.message_handler(func=lambda message: message.text in cart_tags)
def checkout_handler(message):
    answer = get_command_result(message)
    if answer.custom_data is not None:
        for product in answer.custom_data:
            bot.send_photo(message.from_user.id, product.image, product.text, parse_mode='HTML', reply_markup=product.menu)
        bot.send_message(message.from_user.id, "<pre>Для отмены оформления заказа введите \"Отмена\"</pre>\n\n"
                                           "Как к Вам можно обращаться?", parse_mode='HTML')
        bot.register_next_step_handler(message, input_user_name)
    else:
        bot.send_message(message.from_user.id, answer.text, parse_mode='HTML')


# Обработчик успешных платежей
@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    order_id = message.successful_payment.invoice_payload
    wc = WC_API()
    wc.order_pay(order_id)
    db = Database()
    db.clear_user_cart(message.from_user.id)
    bot.send_message(message.chat.id,
                     '<pre>Платеж успешно обработан</pre>\n{0} <b>{1}</b>'.format(
                         message.successful_payment.total_amount / 100, message.successful_payment.currency),
                     parse_mode='HTML')


# Обработчик присланных фотографий, фактически обработчик для команды распознавания цветов
@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    photo_url = bot.get_file(message.photo[-1].file_id).file_path
    file = bot.download_file(photo_url)
    src = f'files/{message.chat.id}_' + photo_url.replace('photos/', '')
    with open(src, 'wb') as new_file:
        new_file.write(file)
    answer = execute_command(message.from_user.id, src,
                             'flower_detection')
    bot.send_message(message.from_user.id, answer.text, parse_mode='HTML')


# Обработчик сообщений, отправленных через бота(via bot), фактически обработчик отправки конкретного товара
@bot.message_handler(func=lambda message: message.via_bot is not None)
def via_bot_message_handler(message):
    answer = get_command_result(message)
    bot.send_photo(message.from_user.id, answer.image, answer.text, parse_mode="HTML", reply_markup=answer.menu)


# Обработчик всех команд, если не сработал никакой из предыдущих, перенаправляется сюда
@bot.message_handler(func=lambda message: True)
def message_handler(message):
    answer = get_command_result(message)
    if answer.image is not None:
        bot.send_photo(message.from_user.id, answer.image, answer.text, parse_mode="HTML", reply_markup=answer.menu)
    else:
        bot.send_message(message.from_user.id, answer.text, reply_markup=answer.menu, parse_mode='HTML')
        if str(answer.custom_data).lower() == "каталог":
            _answer = get_custom_result(message, message.text, "каталог")
            bot.send_message(message.from_user.id, _answer.text, reply_markup=_answer.menu, parse_mode='HTML')


# Обработчик inline-команд
@bot.inline_handler(func=lambda query: len(query.query) > 0)
def inline_handler(query):
    answer = get_inline_command_result(query)
    bot.answer_inline_query(query.id, results=answer.menu)


@bot.callback_query_handler(func=lambda call: call.data.split(":")[0].lower() == "remove_all_from_cart")
def remove_from_cart_callback_handler(call):
    answer = get_callback_command_result(call)
    bot.delete_message(call.from_user.id, call.message.message_id)


# Обработчик добавления в корзину
@bot.callback_query_handler(func=lambda call: call.data.split("=")[0] == "add_to_cart:")
def add_to_cart_callback_handler(call):
    answer = get_callback_command_result(call)
    image = types.InputMedia('photo', answer.image, answer.text)
    bot.edit_message_media(media=image, chat_id=call.from_user.id, message_id=call.message.message_id,
                           reply_markup=answer.menu)


# Обработчик остальных callback-команд
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data != "quantity":
        answer = get_callback_command_result(call)
        bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                      reply_markup=answer.menu)


# Обработчик ошибок оплаты
@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Платеж отклонен")


load_modules()  # Загружаем команды
bot.infinity_polling()  # Запускаем бота
