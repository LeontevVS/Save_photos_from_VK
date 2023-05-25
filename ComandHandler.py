import os
from VK import VK
from YDisk import YDisk
import re

import dotenv

class ComandHandler:

    def __init__(self):
        if not os.path.exists(".env") and  not os.path.isfile(".env"):
            print("Первоначальный ввод токенов.\nТокены будут сохранены в файл .env")
            ComandHandler._set_tokens()
        self._set_handlers()

    def _set_handlers(self):
            dotenv.load_dotenv()
            vk_token = os.getenv("VK_TOKEN")
            vk_api_version = os.getenv("VK_API_VERSION")
            yd_token = os.getenv("YANDEX_TOKEN")
            self.vk_handler = vk_handler = VK(vk_token, vk_api_version)
            self.yd_handler = YDisk(yd_token)
            
    def _set_tokens():
        vk_token = input("Введите вк токен: ")
        vk_api_version = input("Введите версию api вк: ")
        yandex_token = input("Введите токен яндекс диска: ")
        with open(".env", "wt") as file:
            lines = "\n".join([f"VK_TOKEN={vk_token}", f"YANDEX_TOKEN={yandex_token}", f"VK_API_VERSION={vk_api_version}"])
            file.writelines(lines)

    def _upload(self, user_id, count, album):
        pictures = self.vk_handler.get_user_photos(user_id, count, album)
        self.yd_handler.upload_pictures(pictures)

    def handle(self, command):
        match command.split(" ")[0]:
            case "upload":
                user_id = re.search(r"(u:)(\S*)", command)
                if user_id is None:
                    print("Ошибка. Пропущен обязательный параметр")
                    return
                user_id = user_id[2]    
                count = re.search(r"(c:)(\d*)", command)
                count = 5 if count is None else count[2]
                album = re.search(r"(a:)['\"](.*)['\"]", command)
                album = "profile" if album is None else album[2]
                self._upload(user_id, count, album)