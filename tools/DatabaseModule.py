import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT #для автоподтверждения записи

# Класс для работы с базой данных бота POSTGRESQL
class Database:

    def __init__(self):
        self.host = "ec2-52-48-159-67.eu-west-1.compute.amazonaws.com"
        self.database = "dd7qnm4c70adsn"
        self.user = "csvqbwyiddejwm"
        self.password = "6f28b3cd540af6e0714ae55ccbd6aa6fb174074a8257286d9450f0a2f56cfaf6"
        self.port = 5432
        self.connection = None
        self.cursor = None

    # Подключение к бд
    def connect(self):
        self.connection = psycopg2.connect(host=self.host,
                                           database=self.database,
                                           user=self.user,
                                           password=self.password,
                                           port=self.port)
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.connection.cursor()

    # Коризна пользователя
    def get_user_cart_data(self, user_id):
        self.connect()
        cart_id = self.get_user_cart(user_id)
        self.cursor.execute("SELECT product_id, quantity FROM cart WHERE cart_id = " + str(cart_id))
        data = self.cursor.fetchall()
        self.close()
        return data

    # id Корзины пользователя
    def get_user_cart(self, user_id):
        self.cursor.execute("SELECT id FROM user_cart WHERE user_id = " + str(user_id))
        try:
            cart = self.cursor.fetchall()
        except:
            cart = 0
        return cart[0][0]

    # Заносим данные о коризне в БД
    def fill_user_cart(self, user, products, quantity):
        self.connect()
        cart_id = self.get_user_cart(user)
        if cart_id == 0:
            self.user_to_cart(user)
            cart_id = self.get_user_cart(user)
        for i in range(0, len(products)):
            self.cursor.execute("INSERT INTO cart (cart_id, product_id, quantity) VALUES(" + str(cart_id) + ","
                                + str(products[i]) + "," + str(quantity[i]) + ")")
        self.close()

    # Добавление пользователя в БД
    def user_to_cart(self, user_id):
        self.connect()
        self.cursor.execute("INSERT INTO user_cart (user_id) VALUES(" + str(user_id) + ")")
        self.close()

    # Очистка корзины пользователя
    def clear_user_cart(self, user_id):
        self.connect()
        cart_id = self.get_user_cart(user_id)
        self.cursor.execute("DELETE FROM cart WHERE cart_id = " + str(cart_id))
        self.close()

    def set_product_quantity(self, user_id, product, new_quantity):
        self.connect()
        cart_id = self.get_user_cart(user_id)
        self.cursor.execute("UPDATE cart SET quantity = " + str(new_quantity) + " WHERE cart_id = "
                            + str(cart_id) + " AND product_id = " + str(product))
        self.close()

    def remove_product_from_cart(self, user_id, product):
        self.connect()
        cart_id = self.get_user_cart(user_id)
        self.cursor.execute("DELETE FROM cart WHERE cart_id = " + str(cart_id) + " AND product_id = " + str(product))
        self.close()

    # Закрытие подключения
    def close(self):
        self.cursor.close()
        self.connection.close()
