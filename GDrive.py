from datetime import datetime
from Picture import Picture
import urllib.request

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class GDrive:
    def __init__(self):
        auth = GoogleAuth()
        auth.LocalWebserverAuth()
        self.drive = GoogleDrive(auth)        

    def _create_folder_for_upload(self):
        cur_date = datetime.now().strftime("%d.%m.%Y %H-%M-%S")
        folderName = f"Фото из ВК {cur_date}"
        file_metadata = {
            'title': folderName,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = self.drive.CreateFile(file_metadata)
        folder.Upload()
        return folder["id"]

    def upload(self, pictures):
        if pictures is None:
            return
        Picture.set_names_in_list(pictures)
        folder_id = self._create_folder_for_upload()
        pictures_count = len(pictures)
        try:
            for index, picture in enumerate(pictures):
                file_metadata = {
                'title': picture.name,
                'parents': [{'id': folder_id}],
                }
                file = self.drive.CreateFile(file_metadata)
                urllib.request.urlretrieve(picture.url, "temp.jpg")
                file.SetContentFile('temp.jpg')
                file.Upload()
                print(f"Загружено {index+1}/{pictures_count}")
                cur_date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
                Picture.write_log(cur_date, picture)
        except:
            print("Не удалось загрузить")