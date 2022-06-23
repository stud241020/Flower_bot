import woocommerce
from woocommerce import API
import json


# Класс, для получения данных с сайта
class WC_API:

    def __init__(self):
        self.wcapi = API(
            url="https://wp-flowers.ru/",
            consumer_key="", 
            consumer_secret="", 
            timeout=50,
            verify_ssl=False
        )

    def test_get(self, get_str):
        response = self.wcapi.get(get_str)
        return response.json()

    # Получить продукты
    def get_all_products(self):
        response = self.wcapi.get('products')
        return response.json()

    # Получить категории
    def get_categories(self):
        response = self.wcapi.get('products/categories')
        return response.json()

    # Получить конкретный продукт
    def get_product_by_id(self, product_id):
        response = self.wcapi.get('products/' + product_id)
        return response.json()

    # Получить данные о указанных продуктах
    def get_all_products_data(self, products):
        names = dict()
        for item in products:
            names[item['name'].lower()] = item['id']
        return names

    # Оплата заказа
    def order_pay(self, order_id):
        data = {
            "set_paid": True
        }
        self.wcapi.put("orders/" + str(order_id), data)

    # Сделать заказ
    def make_order(self, id, products, name, address, phone):
        data = {
            "payment_method": "bacs",
            "payment_method_title": "Direct Bank Transfer",
            "set_paid": False,
            "billing": {
                "first_name": str(name),
                "last_name": str(id),
                "address_1": "",
                "address_2": "",
                "city": "",
                "state": "",
                "postcode": "",
                "country": "RU",
                "email": "kappa7512@yandex.ru",
                "phone": str(phone)
            },
            "shipping": {
                "first_name": "tg-bot",
                "last_name": str(id),
                "address_1": str(address),
                "address_2": "",
                "city": "",
                "state": "",
                "postcode": "",
                "country": "RU"
            },
            "line_items": [],
            "shipping_lines": [
                {
                    "method_id": "flat_rate",
                    "method_title": "Flat Rate",
                    "total": "0.00"
                }
            ]
        }
        _id = list(products.keys())
        _quantity = list(products.values())
        for i in range(0, len(products)):
            data['line_items'].append({'product_id': int(_id[i]), 'quantity': _quantity[i]})
        order_data = self.wcapi.post("orders", data).json()
        return order_data['id']
