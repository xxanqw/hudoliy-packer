from hashlib import sha1 as sha
from sys import argv as args, exit as shutdown
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox, QMenuBar, QMenu, QHBoxLayout, QProgressBar, QDialog
from PyQt6.QtCore import QThread, Qt, pyqtSignal
from os import system as cmd, path as p
from PyQt6.QtGui import QIcon, QPixmap, QAction
from PyQt6.QtCore import QMimeData, QEvent
from webbrowser import open as web
from requests import get as req
from zipfile import ZipFile as zip

class Downloader(QThread):
    progress_updated = pyqtSignal(int)

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
                    self.progress_updated.emit(progress)

class DownloadWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Завантажувач худолія")
        self.setFixedSize(300, 200)

        self.whatisdown = QLabel("Оскільки мак має приколи з файлами,\nякі використовуються в цьому проекті,\nвам потрібно завантажити їх самостійно.")
        self.wha = QLabel("Жми кнопку, щоб завантажити")
        self.progress_bar = QProgressBar()
        self.download_button = QPushButton("Завантажити")
        self.download_button.clicked.connect(self.start_download)

        layout = QVBoxLayout()
        layout.addWidget(self.whatisdown)
        layout.addWidget(self.wha)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.download_button)
        self.setLayout(layout)

    def start_download(self):
        self.download_button.setEnabled(False)
        cmd("mkdir downloads")
        self.pack_down()
        #self.unzip()

    def pack_down(self):
        self.wha.setText("Завантаження pack.zip")
        url = "https://github.hudoliy.v.ua/"
        name = "pack.zip"
        self.downloader = Downloader(url, name)
        self.downloader.progress_updated.connect(self.update_progress)
        self.downloader.finished.connect(self.Szip_down)
        self.downloader.start()

    def Szip_down(self):
        self.wha.setText("Завантаження 7zip.zip")
        url = "https://assets.hudoliy.v.ua/7zip.zip"
        name = "7zip.zip"
        self.downloader = Downloader(url, name)
        self.downloader.progress_updated.connect(self.update_progress)
        self.downloader.finished.connect(self.unzip)
        self.downloader.start()   

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

    def unzip(self):
        self.wha.setText("Розпаковую..")
        pack_path = "../../../pack"
        Szip_path = "./7zip"
        with zip("downloads/pack.zip", "r") as z:
            z.extractall(pack_path)
        with zip("downloads/7zip.zip", "r") as z:
            z.extractall(Szip_path)
        cmd("chmod +x 7zip/7zz-macos")
        cmd("rm -rf downloads")
        self.close()



class Worker(QThread):
    finished = pyqtSignal(str, str)

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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hudoliy ResourcePacker GUI for macOS (Qt6)")    
        self.setFixedSize(517, 250)
        self.setWindowIcon(QIcon("../Resources/src/icon.ico"))

        self.worker = Worker()
        self.worker.finished.connect(self.show_message)

        self.button_layout = QHBoxLayout()
        self.button = QPushButton("Запакувати та обчислити SHA1")
        self.button.clicked.connect(self.handle_button_click)
        self.button_layout.addWidget(self.button)
        self.button = QPushButton("TEST")
        self.button.clicked.connect(self.show_downloader)
        self.button_layout.addWidget(self.button)

        self.sha1_label = QLabel("SHA1 буде відображено тут")

        logo = QPixmap("../Resources/src/logo.png")
        logo = logo.scaledToWidth(500)
        self.logo_label = QLabel()
        self.logo_label.setPixmap(logo)

        layout = QVBoxLayout()
        layout.addWidget(self.logo_label)
        layout.addLayout(self.button_layout)
        layout.addWidget(self.sha1_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        menu_bar = QMenuBar(self)
        file_menu = QMenu("Файл", self)
        exit_action = QAction("Вихід", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        menu_bar.addMenu(file_menu)
        help_menu = QMenu("Допомога", self)
        github_action = QAction("GitHub", self)
        github_action.triggered.connect(lambda: web('https://github.com/xxanqw/hudoliy-resourcepack'))
        about_action = QAction("Про програму", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(github_action)
        help_menu.addAction(about_action)
        menu_bar.addMenu(help_menu)
        file_menu.addAction(exit_action)
        self.setMenuBar(menu_bar)

        if not p.exists("../../../pack") or not p.isdir("7zip"):
            self.show_downloader()

    def handle_button_click(self):
        self.worker.start()

    def show_message(self, title, message):
        reply = QMessageBox.information(self, title, message)
        if reply == QMessageBox.StandardButton.Ok and title == "Успіх" and message == "Архів zip створено успішно.":
            sha1 = self.worker.calculate_sha1()
            if sha1:
                self.sha1_label.setText(f"SHA1: {sha1}")
                clipboard = QApplication.clipboard()
                mimeData = QMimeData()
                mimeData.setText(sha1)
                clipboard.setMimeData(mimeData)
                self.show_message("Успіх", f"SHA1 скопійовано до буфера обміну. Та записано до файлу sha1.txt.")
    
    def show_about_dialog(self):
        QMessageBox.about(self, "Про програму", "Hudoliy ResourcePacker GUI (Qt6)\n\nАвтор: xxanqw\n\nGitHub: https://github.com/xxanqw/hudoliy-resourcepack")

    def show_downloader(self):
        self.downloader = DownloadWindow()
        self.downloader.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.downloader.show()

if __name__ == "__main__":
    app = QApplication(args)
    window = MainWindow()
    window.show()
    shutdown(app.exec())