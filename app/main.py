from hashlib import sha1 as sha
from sys import platform as target, argv as args, exit as shutdown
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox, QMenuBar, QMenu, QHBoxLayout, QDialog, QProgressBar
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from os import system as cmd, path as p
from PyQt6.QtGui import QIcon, QPixmap, QAction
from PyQt6.QtCore import QMimeData
from webbrowser import open as web
from zipfile import ZipFile as zip
from requests import get as req

class Cleaner(QThread):
    def run(self):
        if target == "win32":
            cmd("del /Q /S downloads")
        elif target == "linux" or target == "linux2":
            cmd("rm -rf usr/bin/downloads/*")

class Unzipper(QThread):
    def __init__(self, file, path):
        super().__init__()
        self.file = file
        self.path = path
    
    def run(self):
        with zip(self.file, "r") as z:
            z.extractall(self.path)

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
        if target == "win32":
            with open(f'downloads/{self.name}', 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
                        bytes_downloaded += len(chunk)
                        progress = int((bytes_downloaded / total_size) * 100)
                        self.progress_updated.emit(progress)
        elif target == "linux" or target == "linux2":
            with open(f'usr/bin/downloads/{self.name}', 'wb') as file:
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
        self.setFixedSize(350, 150)
        if target == "win32":
            self.setWindowIcon(QIcon("./src/pack.ico"))
        elif target == "linux" or target == "linux2":
            self.setWindowIcon(QIcon("./usr/bin/src/pack.ico"))

        self.whatisdown = QLabel("Програма потребує додаткових файлів для роботи.")
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
        if target == "win32":
            cmd("mkdir downloads")
        elif target == "linux" or target == "linux2":
            cmd("mkdir usr/bin/downloads")
        self.pack_down()

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
    
    def chmod(self):
        cmd("chmod +x usr/bin/7zip/7zz-linux")

    def unzip(self):
        self.wha.setText("Розпаковую..")
        pack_path = "pack"
        Szip_path = "7zip"
        if target == "win32":
            self.unzipper = Unzipper(path=pack_path, file="downloads/pack.zip")
        elif target == "linux" or target == "linux2":
            self.unzipper = Unzipper(path=pack_path, file="usr/bin/downloads/pack.zip")
        self.unzipper.start()
        if target == "win32":
            self.unzip_7zip = Unzipper(path=Szip_path, file="downloads/7zip.zip")
        elif target == "linux" or target == "linux2":
            self.unzip_7zip = Unzipper(path=Szip_path, file="usr/bin/downloads/7zip.zip")
        self.unzip_7zip.start()
        if target == "linux" or target == "linux2":
            self.unzip_7zip.finished.connect(self.chmod)

        QMessageBox.information(self, "Успіх", "Файли завантажено та розпаковано успішно.")
        self.clean_up = Cleaner()
        self.clean_up.start()
        self.clean_up.finished.connect(self.close)

class AdditionalWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Додаткові фішечки")
        self.setFixedSize(400, 200)
        if target == "win32":
            self.setWindowIcon(QIcon("./src/pack.ico"))
        elif target == "linux" or target == "linux2":
            self.setWindowIcon(QIcon("./usr/bin/src/pack.ico"))

        self.desc = QLabel("Це поки що в розробці\nАле вже можна скачати текстурки майна для референсів")
        self.resource = QLabel("Дефолтні текстури майна")
        self.resource_button = QPushButton("Завантажити")
        self.resource_button.clicked.connect(self.download_resource)
        self.progress_bar = QProgressBar()
        self.progress_bar.hide()

        layout = QVBoxLayout()
        layout.addWidget(self.desc)
        layout.addStretch()
        flexlayout = QHBoxLayout()
        flexlayout.addWidget(self.resource, alignment=Qt.AlignmentFlag.AlignLeft)
        flexlayout.addWidget(self.resource_button, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.progress_bar)
        layout.addLayout(flexlayout)
        self.setLayout(layout)

    def download_resource(self):
        self.resource_button.setEnabled(False)
        self.progress_bar.show()
        url = "https://assets.hudoliy.v.ua/resources.zip"
        name = "resources.zip"
        self.downloader = Downloader(url, name)
        self.downloader.progress_updated.connect(self.update_progress)
        self.downloader.finished.connect(self.unzip)
        self.downloader.start()

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

    def unzip(self):
        self.progress_bar.hide()
        if target == "win32":
            self.unzipper = Unzipper(path="pack", file="downloads/resources.zip")
        elif target == "linux" or target == "linux2":
            self.unzipper = Unzipper(path="pack", file="usr/bin/downloads/resources.zip")
        self.unzipper.start()
        QMessageBox.information(self, "Успіх", "Текстури майна завантажено та розпаковано успішно.")
        self.resource_button.setEnabled(True)
        self.clean_up = Cleaner()
        self.clean_up.start()

class Worker(QThread):
    finished = pyqtSignal(str, str)

    def run(self):
        try:
            if target == "win32":
                cmd("7zip\\7za.exe a pack.zip .\pack\*")
            elif target == "linux" or target == "linux2":
                cmd("usr/bin/7zip/7zz-linux a pack.zip ../pack/*")
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
        if target == "win32":
            sha1 = self.get_sha1("pack.zip")
        elif target == "linux" or target == "linux2":
            sha1 = self.get_sha1("../pack.zip")
        if sha1:
            if target == "win32":
                with open("sha1.txt", "w") as f:
                    f.write(sha1)
                    f.close
            elif target == "linux" or target == "linux2":
                with open("../sha1.txt", "w") as f:
                    f.write(sha1)
                    f.close
            return sha1

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        if target == "win32":
            self.setWindowTitle("Hudoliy ResourcePacker GUI for Windows (Qt6)")
        elif target == "linux" or target == "linux2":
            self.setWindowTitle("Hudoliy ResourcePacker GUI for Linux (Qt6)")
        self.setFixedSize(517, 250)
        if target == "win32":
            self.setWindowIcon(QIcon("./src/pack.ico"))
        elif target == "linux" or target == "linux2":
            self.setWindowIcon(QIcon("./usr/bin/src/pack.ico"))

        self.worker = Worker()
        self.worker.finished.connect(self.show_message)

        self.button_layout = QHBoxLayout()
        self.button = QPushButton("Запакувати та обчислити SHA1")
        self.button.clicked.connect(self.handle_button_click)
        self.button_layout.addWidget(self.button)
        self.additional_button = QPushButton("Додаткові фішечки")
        self.additional_button.clicked.connect(self.show_additional)
        self.button_layout.addWidget(self.additional_button)

        self.sha1_label = QLabel("SHA1 буде відображено тут")

        if target == "win32":
            logo = QPixmap("./src/logo.png")
        elif target == "linux" or target == "linux2":
            logo = QPixmap("./usr/bin/src/logo.png")
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
        if target == "win32":
            exit_action.setIcon(QIcon("./src/logout.png"))
        elif target == "linux" or target == "linux2":
            exit_action.setIcon(QIcon("./usr/bin/src/logout.png"))
        menu_bar.addMenu(file_menu)
        help_menu = QMenu("Допомога", self)
        github_action = QAction("GitHub", self)
        github_action.triggered.connect(lambda: web('https://github.com/xxanqw/hudoliy-resourcepack'))
        if target == "win32":
            github_action.setIcon(QIcon("./src/github-logo.png"))
        elif target == "linux" or target == "linux2":
            github_action.setIcon(QIcon("./usr/bin/src/github-logo.png"))
        about_action = QAction("Про програму", self)
        about_action.triggered.connect(self.show_about_dialog)
        if target == "win32":
            about_action.setIcon(QIcon("./src/info-button.png"))
        elif target == "linux" or target == "linux2":
            about_action.setIcon(QIcon("./usr/bin/src/info-button.png"))
        help_menu.addAction(github_action)
        help_menu.addAction(about_action)
        menu_bar.addMenu(help_menu)
        file_menu.addAction(exit_action)
        self.setMenuBar(menu_bar)
        if target == "win32":
            if not p.exists("pack") or not p.isdir("7zip"):
                self.show_downloader()
        elif target == "linux" or target == "linux2":
            if not p.exists("../pack") or not p.isdir("usr/bin/7zip"):
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

    def show_additional(self):
        self.additional = AdditionalWindow()
        self.additional.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.additional.show()

app = QApplication(args)
window = MainWindow()
window.show()
shutdown(app.exec())