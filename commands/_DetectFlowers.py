import tools.CommandSystem as command_system
from tools.CommandResult import CommandResult


# Вывод информации о распознавании
def _detect_flower(id, text):
    result = CommandResult("<b>Представляем вам нашу новую тестовую функцию:</b>\n\n"
                           "<u>Определение вида цветка на фотографии!</u>\n\n"
                           "<i>Просто загрузите фотографию, а дальше наш бот все сделает сам.</i>\n\n"
                           "<pre language=\"python\">На данный момент поддерживается распознавание одуванчиков, "
                           "ромашек, тюльпанов, подсолнухов и роз.</pre>")
    return result


_detect_flower_command = command_system.Command()

_detect_flower_command.keys = ['Распознавание цветов', u'\U0001F33C Распознавание цветов']
_detect_flower_command.description = 'Определяет вид цвета на фотографии'
_detect_flower_command.process = _detect_flower
