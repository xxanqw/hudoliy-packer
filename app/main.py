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
import random
import string

class Cleaner(QThread):
    def run(self):
        if target == "win32":
            cmd("del /Q /S downloads")
        elif target == "linux" or target == "linux2":
            cmd("rm -rf downloads/*")

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
        self.setFixedSize(350, 150)
        icon = p.join(p.dirname(__file__), "src/pack.ico")
        self.setWindowIcon(QIcon(icon))

        self.whatisdown = QLabel("Програма потребує додаткових файлів.")
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
        cmd("chmod +x 7zip/7zz-linux")

    def unzip(self):
        self.wha.setText("Розпаковую..")
        pack_path = "pack"
        Szip_path = "7zip"
        self.unzipper = Unzipper(path=pack_path, file="downloads/pack.zip")
        self.unzipper.start()
        self.unzip_7zip = Unzipper(path=Szip_path, file="downloads/7zip.zip")
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
        icon = p.join(p.dirname(__file__), "src/pack.ico")
        self.setWindowIcon(QIcon(icon))

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
        self.unzipper = Unzipper(path="defaultpack", file="downloads/resources.zip")
        self.unzipper.start()
        QMessageBox.information(self, "Успіх", "Текстури майна завантажено та розпаковано успішно.")
        self.resource_button.setEnabled(True)
        self.clean_up = Cleaner()
        self.clean_up.start()

class Worker(QThread):
    finished = pyqtSignal(str, str)

    def run(self):
        try:
            cmd("7zip\\7za.exe a pack.zip .\pack\*")
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
        sha1 = self.get_sha1("pack.zip")
        if sha1:
            with open("sha1.txt", "w") as f:
                f.write(sha1)
                f.close
            return sha1
        
    def generate_uuid(self):
        if not p.exists("uuid.txt"):
            def generate_random_string(length):
                letters = string.ascii_letters + string.digits + "-"
                return ''.join(random.choice(letters) for _ in range(length))

            uuid = f"{generate_random_string(8)}-{generate_random_string(4)}-4{generate_random_string(3)}-{generate_random_string(4)}-{generate_random_string(12)}"
            if uuid:
                with open("uuid.txt", "w") as f:
                    f.write(uuid)
                    f.close
            return uuid
        elif p.exists("uuid.txt"):
            with open("uuid.txt", "r") as f:
                return f.read()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        if target == "win32":
            self.setWindowTitle("Hudoliy ResourcePacker GUI for Windows (Qt6)")
        elif target == "linux" or target == "linux2":
            self.setWindowTitle("Hudoliy ResourcePacker GUI for Linux (Qt6)")
        self.setFixedSize(517, 260)
        icon = p.join(p.dirname(__file__), "src/pack.ico")
        self.setWindowIcon(QIcon(icon))


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
        self.UUID_label = QLabel("UUID буде відображено тут")

        logo_path = p.join(p.dirname(__file__), "src/logo.png")
        logo = QPixmap(logo_path)
        logo = logo.scaledToWidth(500)
        self.logo_label = QLabel()
        self.logo_label.setPixmap(logo)

        layout = QVBoxLayout()
        layout.addWidget(self.logo_label)
        layout.addLayout(self.button_layout)
        layout.addWidget(self.sha1_label)
        layout.addWidget(self.UUID_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        menu_bar = QMenuBar(self)

        file_menu = QMenu("Файл", self)

        exit_action = QAction("Вихід", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        exit_icon = p.join(p.dirname(__file__), "src/logout.png")
        exit_action.setIcon(QIcon(exit_icon))

        menu_bar.addMenu(file_menu)

        help_menu = QMenu("Допомога", self)

        github_action = QAction("GitHub", self)
        github_action.triggered.connect(lambda: web('https://github.com/xxanqw/hudoliy-resourcepack'))
        github_icon = p.join(p.dirname(__file__), "src/github-logo.png")
        github_action.setIcon(QIcon(github_icon))

        about_action = QAction("Про програму", self)
        about_action.triggered.connect(self.show_about_dialog)
        about_icon = p.join(p.dirname(__file__), "src/info-button.png")
        about_action.setIcon(QIcon(about_icon))

        help_menu.addAction(github_action)
        help_menu.addAction(about_action)
        menu_bar.addMenu(help_menu)
        file_menu.addAction(exit_action)
        self.setMenuBar(menu_bar)

        if not p.exists("pack") or not p.isdir("7zip"):
            self.show_downloader()

    def handle_button_click(self):
        self.worker.start()

    def show_message(self, title, message):
        reply = QMessageBox.information(self, title, message)
        if reply == QMessageBox.StandardButton.Ok and title == "Успіх" and message == "Архів zip створено успішно.":
            sha1 = self.worker.calculate_sha1()
            uuid = self.worker.generate_uuid()
            if sha1:
                self.sha1_label.setText(f"SHA1: {sha1}")
                self.UUID_label.setText(f"UUID: {uuid}")
                clipboard = QApplication.clipboard()
                mimeData = QMimeData()
                mimeData.setText(sha1)
                clipboard.setMimeData(mimeData)
                self.show_message("Успіх", f"SHA1 скопійовано до буфера обміну. Та записано до файлу sha1.txt.\nТакож згенеровано UUID та записано до файлу uuid.txt.")
    
    def show_about_dialog(self):
        QMessageBox.about(self, "Про програму", "Hudoliy ResourcePacker GUI (Qt6)\n\nАвтор: xxanqw\n\nGitHub: https://github.com/xxanqw/hudoliy-packer")

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