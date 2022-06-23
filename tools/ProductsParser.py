import re
html_remover = re.compile('<.*?>')  # Убрать html


# Разбор данных продуктов
class ProductsParser:

    # Получить категорию продукта
    @staticmethod
    def get_category_of_product(product):
        return product['categories'][0]['id']

    # Фильтр по категориям
    @staticmethod
    def category_filter(products, category):
        filtrated_products = []
        for product in products:
            if ProductsParser.get_category_of_product(product) == category:
                filtrated_products.append(product)
        return filtrated_products

    # Общий метод для получения любых данных
    @staticmethod
    def get_custom_data(json_dict, key):
        temp_arr = []
        for item in json_dict:
            temp_arr.append(item[key])
        return temp_arr

    # Получить имена категорий
    @staticmethod
    def get_categories_names(categories):
        return ProductsParser.get_custom_data(categories, "name")

    # Получить id категорий
    @staticmethod
    def get_categories_id(categories):
        return ProductsParser.get_custom_data(categories, "id")

    # Убрать html из текста
    @staticmethod
    def remove_html_from_text(text):
        clean_text = re.sub(html_remover, '', text)
        return clean_text

