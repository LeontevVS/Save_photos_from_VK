from datetime import datetime
import json

import requests
import tzlocal

class Picture:

    def __init__(self, date, url, likes_count, size, width, height):
        self.url = url
        self.size = size
        self.height = height
        self.width = width
        self.likes_count = likes_count
        self._set_date(date)

    def set_names_in_list(pictures):
        for picture in pictures:
            if len(list(filter(lambda x: x.likes_count == picture.likes_count, pictures))) > 1:
                picture.name = f"{picture.likes_count} {picture.date}.jpg"
            else:
                picture.name = f"{picture.likes_count}.jpg"

    def write_log(date, picture):
        picture_info = {
                "vk_load_date": picture.date,
                "yandex_load_date": date,
                "url": picture.url,
                "likes_count": picture.likes_count,
                "size": picture.size,
                "width": picture.width,
                "height": picture.height,
                "name": picture.name
            }
        with open("log.jsonlines", "at", encoding="utf-8") as file:
            json.dump(picture_info, file)
            file.write("\n")

    def _set_date(self, unix_date):
        unix_date = float(unix_date)
        local_timezone = tzlocal.get_localzone()
        local_date = datetime.fromtimestamp(unix_date, local_timezone)
        self.date = local_date.strftime("%d-%m-%Y %H-%M-%S")

    def get_photo(self):
        response = requests.get(url=self.url)
        return response.content