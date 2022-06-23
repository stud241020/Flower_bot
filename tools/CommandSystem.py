command_list = []  # Список команд
command_list_keys = []  # Список ключей команд

# Класс, реализующий систему команд
class Command:

   def __init__(self):
       self.__keys = []
       self.description = ''
       command_list.append(self)

   @property
   def keys(self):
       return self.__keys

   @keys.setter
   def keys(self, mas):
       for k in mas:
           self.__keys.append(k.lower())
           command_list_keys.append(k.lower())

   def process(self, id, text):
       pass