import tools.CommandSystem as command_system
from gui.MainGui import MainGUI
from tools.CommandResult import CommandResult
from tools.DatabaseModule import Database


# Начало
def start(id, text):
    try:  # Добавляем юзера в бд
        db = Database()
        db.user_to_cart(id)
    except:
        print(str(id) + " уже добавлен")
    result = CommandResult("Выберите действие:", menu=MainGUI.get_main_menu())
    return result


start_command = command_system.Command()

start_command.keys = ['/start']
start_command.description = 'Начало'
start_command.process = start
