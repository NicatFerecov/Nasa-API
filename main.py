import requests
import re
from datetime import datetime
from deep_translator import GoogleTranslator
import json
from PIL import Image


class Nasa:
    _FORMAT_YAML = {
        "String" : str,
        "Integer" : int,
        "Float" : float,
        "Bool" : bool
    }
    nasaTitle = [] # bos list
    _translated_text = [] # bos list
    _IMAGE_URL = [] # bos list
    def __init__(self, date):  
        self.api_key = "IZEbkct7cfPaRY2HXDn6GhhFsd70yCIeR8nAJUpn" # Your API key
        self.date = date
        self.url = f"https://api.nasa.gov/planetary/apod?api_key={self.api_key}&date={self.date}"
    def response_url(self):
        if not len(self.url) == 0:
            response = requests.get(self.url)
            data = response.json()
            self._IMAGE_URL.append(data["url"])
            self.nasaTitle.append(data["title"])
            return data["title"] + " " + data["explanation"]
        else:
            raise ValueError("Xeta")
    def download_image(self, url, save_as):
        response = requests.get(url)
        with open(save_as, 'wb') as file:
            file.write(response.content)
    def translate(self, text: str) -> str:
        if len(text) > 4:
            translated_text = GoogleTranslator(source='auto', target='az').translate(text)
            self._translated_text.append(translated_text)
            if type(translated_text) == str:
                return translated_text.strip()
        else:
            return None
    def nasa_info(self):
        main_info = {
            "text" : self.nasaTitle[0],
            "url" : self._IMAGE_URL[0]
        }
        if len(main_info["text"]) > 5:
            return main_info
        else:
            return None
    def save_to_file(self, format: str):
        if format == "json":
            with open("nasa_info.json", "a", encoding="utf-8") as nasafile:
                json.dump(self.nasa_info(), nasafile, indent=4, ensure_ascii=False)
        elif format == "txt":
            with open("nasa_info.txt", "a", encoding="utf-8") as files:
                files.write(self._translated_text[0])
        else:
            raise ValueError("Xeta.")
    def show_image(self, path: str):
        img = Image.open(path)
        print(img.show())
    def search_engine(self):
        url = "https://www.searchapi.io/api/v1/search"
        params = {
          "engine": "google",
          "q": self.nasaTitle[0],
          "api_key": "6FQ94D6stc8dCSsf86jCkqrZ" # Your API key
        }

        response = requests.get(url, params=params)
        search_r = response.json()
        with open("searchResult.json", "a", encoding="utf-8") as files:
            json.dump(search_r["organic_results"], files, indent=4, ensure_ascii=False)
        with open("searchMetaData.json", "a") as meta:
            json.dump(search_r["search_metadata"], meta, indent=4, ensure_ascii=False)


    

 
PATH_NAME = 'image.jpg' # image name

nasa = Nasa(date="2022-09-13")
print(nasa.translate(text=nasa.response_url()))
nasa.download_image(url=nasa._IMAGE_URL[0], save_as=PATH_NAME)
nasa.save_to_file(format="json")
# nasa.search_engine()