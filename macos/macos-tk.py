from customtkinter import *
from PIL import Image
from os import system as cmd
from os import path as p
from hashlib import sha1 as sha
from requests import get as req



class AdvancedWindow(CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Розширені налаштування")
        self.geometry("300x300")
        self.resizable(False, False)

        self.label = CTkLabel(self, text="Тут будуть розширені налаштування")
        self.label.pack(pady=10)

class Worker():
    def run(self):
        try:
            cmd("7zip/7zz-macos a ../../../pack.zip ../../../pack/*")
            self.finished.emit("Успіх", "Архів zip створено успішно.")
        except Exception as e:
            self.finished.emit("Помилка", f"Не вдалося створити архів zip: {e}")

    def get_sha1(self, file_name):
        try:
            with open(file_name, "rb") as f:
                sha1 = sha()
                for chunk in iter(lambda: f.read(4096), b""):
                    sha1.update(chunk)
            return sha1.hexdigest()
        except Exception as e:
            self.finished.emit("Помилка", f"Не вдалося розрахувати SHA1-хеш: {e}")
            return None

    def calculate_sha1(self):
        sha1 = self.get_sha1("../../../pack.zip")
        if sha1:
            with open("../../../sha1.txt", "w") as f:
                f.write(sha1)
                f.close
            return sha1

class Downloader():
    def __init__(self, url, name):
        super().__init__()
        self.url = url
        self.name = name

    def run(self):
        response = req(self.url, stream=True)
        total_size = int(response.headers.get('Content-Length', 0))
        bytes_downloaded = 0

        with open(f'downloads/{self.name}', 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    bytes_downloaded += len(chunk)
                    progress = int((bytes_downloaded / total_size) * 100)

class DownloadWindow(CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Завантаження")
        self.geometry("300x140")
        self.resizable(False, False)

        self.label = CTkLabel(self, text="Завантаження необхідних файлів...")
        self.label.pack(pady=10)
        self.progress = CTkProgressBar(self, mode="normal")
        self.progress.pack(pady=10)
        self.download_button = CTkButton(self, text="Завантажити", command=self.Szip_down)
        self.download_button.pack(pady=10)
    
    def Szip_down(self):
        url = "https://assets.hudoliy.v.ua/7zip.zip"
        name = "7zip.zip"
        self.downloader = Downloader(url, name)


class MainWindow(CTk):
    def __init__(self):
        super().__init__()

        self.title("Худолій Пакер")
        self.geometry("600x300")
        self.resizable(False, False)

        self.logo = CTkImage(light_image=Image.open("./src/logo.png"), dark_image=Image.open("./src/logo.png"), size=(520, 150))
        self.logo = CTkLabel(self, text="", image=self.logo)
        self.grid_columnconfigure((0,1), weight=1)
        self.logo.grid(row=0, column=0, pady=10, columnspan=2)
        self.pack_button = CTkButton(self, text="Запакувати і хешувати", command=self.pack)
        self.pack_button.grid(row=1, column=0, pady=10, padx=10, sticky="ew")
        self.advanced_button = CTkButton(self, text="Розширені налаштування", command=self.advanced)
        self.advanced_button.grid(row=1, column=1, pady=10, padx=10, sticky="ew")
        self.sha1 = CTkLabel(self, text="SHA1 буде відображено тут", font=("Arial", 12))
        self.sha1.grid(row=2, column=0, pady=10, padx=10, sticky="ew", columnspan=2)

        if not p.exists("../../../pack") or not p.exists("7zip/7zz-macos"):
            self.show_download()
    def pack(self):
        pass

    def advanced(self):
        self.advanced_window = AdvancedWindow()
        self.advanced_window.grab_set()
        self.advanced_window.mainloop()

    def show_download(self):
        self.download_window = DownloadWindow()
        self.download_window.grab_set()
        self.download_window.mainloop()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
