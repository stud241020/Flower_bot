# Класс, представляющий транспорт для результата команд
class CommandResult:

    def __init__(self, text="",
                 image=None,
                 menu=None,
                 products=None,
                 custom_data=None):
        self.text = text
        self.image = image
        self.menu = menu
        self.custom_data = custom_data
        self.products = products
