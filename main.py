import os
import requests
import arcade
from utils import get_spn

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 450
WINDOW_TITLE = "Полный поиск"
MAP_FILE = "map.png"


class MapWindow(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        self.background = None

    def setup(self):
        address = input("Введите адрес: ")

        geocoder_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
            "geocode": address,
            "format": "json"
        }

        response = requests.get(geocoder_server, params=geocoder_params)
        json_data = response.json()

        toponym = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        coords = toponym["Point"]["pos"].replace(" ", ",")

         spn = get_spn(toponym)

        static_server = "https://static-maps.yandex.ru/v1"
        map_params = {
            "apikey": "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13",
            "ll": coords,
            "spn": spn,
            "pt": f"{coords},pm2rdl"
        }

        map_response = requests.get(static_server, params=map_params)

        with open(MAP_FILE, "wb") as f:
            f.write(map_response.content)

        self.background = arcade.load_texture(MAP_FILE)

    def on_draw(self):
        self.clear()
        if self.background:
            arcade.draw_texture_rect(
                self.background,
                arcade.LBWH(0, 0, self.width, self.height)
            )


def main():
    window = MapWindow()
    window.setup()
    arcade.run()
    if os.path.exists(MAP_FILE):
        os.remove(MAP_FILE)


if __name__ == "__main__":
    main()