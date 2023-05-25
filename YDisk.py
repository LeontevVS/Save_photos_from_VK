from datetime import datetime
from Picture import Picture

import requests

class YDisk:

    def __init__(self, token):
        self.token = token
        self.base_url = "https://cloud-api.yandex.net/v1/disk/resources/"
        self._set_headers()

    def _set_headers(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f"OAuth {self.token}"
        }
        self.headers = headers

    def _create_folder(self):
        cur_date = datetime.now().strftime("%d.%m.%Y %H-%M-%S")
        path = f"/Фото из ВК {cur_date}"
        url = self.base_url
        params = {"path": path}
        response = requests.put(url=url, params=params, headers=self.headers)
        self.folder_path = path

    def _get_link_to_upload(self, file_name):
        url = f"{self.base_url}upload"
        headers = self.headers
        path = f"{self.folder_path}/{file_name}"
        params = {"path": path, 'overwrite': 'true'}
        response = requests.get(url=url, params=params, headers=headers)
        response_json = response.json()
        link = dict(response_json)['href']
        return link

    def upload_pictures(self, pictures):
        if pictures is None:
            return
        self._create_folder()
        Picture.set_names_in_list(pictures)
        pictures_count = len(pictures)
        for index, picture in enumerate(pictures):
            url = self._get_link_to_upload(picture.name)
            data = picture.get_photo()
            response = requests.put(url=url, data=data)
            response.raise_for_status()
            if response.status_code == 201:
                print(f"Загружено {index+1}/{pictures_count}")
                cur_date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
                Picture.write_log(cur_date, picture)