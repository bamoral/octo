import requests

sp = ['Барнаул', 'Мелеуз', 'Йошкар-Ола']
for city in sp:
    geocoder_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode" \
                       f"={city}&format=json"
    response = requests.get(geocoder_request)

    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["Components"][2]['name']
        print(toponym_address)
    else:
        print("Ошибка выполнения запроса:")
        print(geocoder_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")