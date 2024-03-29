import os
import sys
import requests


def get_image(coords, size):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={coords}&spn={size},0.002&l=map"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запишем полученное изображение в файл.
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    # возврааем картинку
    return map_file
