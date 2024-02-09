from hashlib import sha1 as sha
from sys import platform as target
from sys import argv as args
from sys import exit as shutdown
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox, QMenuBar, QMenu, QHBoxLayout
from PyQt6.QtCore import QThread, pyqtSignal
from os import system as cmd
from PyQt6.QtGui import QIcon, QPixmap, QAction
from PyQt6.QtCore import QMimeData
from webbrowser import open as web

class Worker(QThread):
    finished = pyqtSignal(str, str)

    def run(self):
        try:
            if target == "win32":
                cmd("7zip\\7za.exe a pack.zip .\pack\*")
            elif target == "linux" or target == "linux2":
                cmd("7zip/7zz-linux a pack.zip ./pack/*")
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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        if target == "win32":
            self.setWindowTitle("Hudoliy ResourcePacker GUI for Windows (Qt6)")
        elif target == "linux" or target == "linux2":
            self.setWindowTitle("Hudoliy ResourcePacker GUI for Linux (Qt6)")
        self.setFixedSize(517, 250)
        self.setWindowIcon(QIcon("./app/src/pack.ico"))

        self.worker = Worker()
        self.worker.finished.connect(self.show_message)

        self.button_layout = QHBoxLayout()
        self.button = QPushButton("Запакувати та обчислити SHA1")
        self.button.clicked.connect(self.handle_button_click)
        self.button_layout.addWidget(self.button)

        self.sha1_label = QLabel("SHA1 буде відображено тут")

        logo = QPixmap("./app/src/logo.png")
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

app = QApplication(args)
window = MainWindow()
window.show()
shutdown(app.exec())