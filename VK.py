from Picture import Picture

import requests

class VK:

    _MAX_PHOTOS_IN_REQUEST = 1000

    def __init__(self, token, version):
        self._set_base_args(token, version)
    
    def _set_base_args(self, token, version):
        self.base_params = {
                "access_token": token,
                "v": version
        }
        self.base_url = "https://api.vk.com/method/"

    def get_user_info(self, user_id):
        url = f"{self.base_url}users.get"
        params = {
            **self.base_params,
            "user_ids": user_id
        }
        response = requests.post(url=url, params=params).json()
        return response

    def _get_not_system_album_id(self, owner_id, title):
        try:
            url = f"{self.base_url}photos.getAlbums"
            params = {
                **self.base_params,
                "owner_id": owner_id,
                "need_system": 1
            }
            response = requests.post(url=url, params=params).json()["response"]
            return response
        except IndexError:
            print("Альбом не найден")

    def _collect_maxsized_images(response):
        try:
            items = response["response"]["items"]
            result = []
            for item in items:
                max_size = item["sizes"][-1]
                result.append(Picture(
                    item["date"], 
                    max_size["url"], 
                    item["likes"]["count"],
                    max_size["type"],
                    max_size["width"],
                    max_size["height"]))
            return result
        except KeyError:
            print("Не удалось получить фото из ВК")

    def get_user_photos(self, user_id, count, album):
        try:
            user_info = self.get_user_info(user_id)
            if "error" in user_info.keys():
                print("Ошибка авторизации")
                return
            if len(user_info["response"]) == 0:
                print("Пользователь с данным id не найден")
                return
            owner_id = user_info["response"][0]["id"]
            if album != 'profile' and album != 'wall':
                album_info = self._get_not_system_album_id(owner_id, album)
                finded_album = list(filter(lambda x: x["title"] == album, album_info["items"]))
                if len(finded_album) != 0:
                    album = finded_album[0]["id"]
                else:
                    print(f"Альбом с названием {album} не найден у пользователя")
                    return
            photos = self._get_user_photos_request(owner_id, count, album)
            return photos
        except:
            return

    def _get_user_photos_request(self, owner_id, count, album_id):
        params = {
            **self.base_params,
            "owner_id": owner_id, 
            "count": count, 
            "album_id": album_id,
            "rev": 1,
            "extended": 1
        }
        url = f"{self.base_url}photos.get"
        photos = list()
        count = int(count)
        if count > VK._MAX_PHOTOS_IN_REQUEST:
            offset = 0
            count_per_request = VK._MAX_PHOTOS_IN_REQUEST
            while count != 0:
                params["offset"] = offset
                params['count'] = count_per_request
                response = requests.post(url=url,params=params).json()
                photos += VK._collect_maxsized_images(response)
                offset += VK._MAX_PHOTOS_IN_REQUEST
                count -= count_per_request
                if count < VK._MAX_PHOTOS_IN_REQUEST:
                    count_per_request = count    
            return photos
        else:
            response = requests.post(url=url,params=params).json()
            photos = VK._collect_maxsized_images(response)
            return photos