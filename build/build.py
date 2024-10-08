from sys import platform as target
from os import system as cmd, getcwd as dir, chdir as cd
from os.path import basename as cdn
from os import chdir as cd

def build():
    input("\nЗверніть увагу що скрипт білдить програму для вашої ОС.\nНатисніть Enter щоб почати збірку...")

    print(f"\nЗбірка для {osname()}...\n")
    if target == "win32":
        cmd('python -m nuitka --onefile --follow-imports --enable-plugin=pyqt6 -o main --output-dir=../app/ --windows-icon-from-ico=../app/src/pack.ico --windows-console-mode=disable --deployment --company-name=xxanqw --product-name="Hudoliy ResourcePacker GUI for Windows (Qt6)" --product-version=0.1.21.1 --include-data-dir=../app/src=src ../app/main.py')
    elif target == "linux" or target == "linux2":
        cmd('python -m nuitka --onefile --follow-imports --enable-plugin=pyqt6 -o main --output-dir=../app/ --deployment --include-data-dir=../app/src=src ../app/main.py')
    print(f"\nЗбірка для {osname()} завершена.\n")

def osname():
    if target == "win32":
        return "Windows"
    elif target == "linux" or target == "linux2":
        return "Linux"

def main():
    current_directory = dir()
    current_directory_name = cdn(current_directory)
    print("Hudoliy ResourcePacker GUI builder\n==================================\n")

    expected_directory = "build"
    if current_directory_name != expected_directory:
        print("Ви запустили скрипт не з тієї папки, в якій він знаходиться.")
        if current_directory_name == "hudoliy-packer":
            input("Оскільки ви знаходитесь в кореневій папці натисніть Enter аби змінити папку на build та запустити скріпт...")
            cd(expected_directory)
            build()
    else:
        build()

def cls():
    if target == "win32":
        cmd("cls")
    if target == "linux" or target == "linux2":
        cmd("clear")

if __name__ == "__main__":
    cls()
    main()