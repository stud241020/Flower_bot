import tools.CommandSystem as command_system
from tools.CommandResult import CommandResult
from tensorflow import keras
import numpy as np
import cv2

classes = [u'Одуванчик', 'Ромашка', 'Тюльпан', 'Подсолнух', u'\U0001F339 Роза']  # Цветы доступные для распознавания
model = keras.models.load_model(r'files\flowers_net\flowers_model.h5')  # Загрузка модели
img_size = 224  # Размер изображения


# Распознавание цветка
def detect_flower(id, text):
    photo = cv2.imread(text, cv2.IMREAD_COLOR)  # Считывание картинки
    resize_arr = cv2.resize(photo, (img_size, img_size))  # Ресайз
    x = np.array(resize_arr) / 255  # Картинку в массив
    x = x.reshape(-1, img_size, img_size, 3)  # Переделываем массив в трехмерный
    _predict = model.predict(x)  # Определяем
    predict = np.argmax(_predict, axis=1)   # Переводим результат в целове число
    result = CommandResult("На фотографии: <b>" + classes[predict[0]] + "</b>")
    return result


detect_flower_command = command_system.Command()

detect_flower_command.keys = ['flower_detection', 'распознавание цветка']
detect_flower_command.description = 'Определяет вид цвета на фотографии'
detect_flower_command.process = detect_flower
