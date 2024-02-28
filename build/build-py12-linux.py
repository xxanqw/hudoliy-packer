from sys import platform as target
from os import system as cmd, getcwd as dir, chdir as cd
from os.path import basename as cdn
from os import chdir as cd

def build():
    input("Натисніть Enter щоб почати збірку...")

    print(f"\nЗбірка для {osname()}...\n")
    cmd('pyinstaller ../app/main.py --distpath ../app/ -y --clean -F')
    print(f"\nЗбірка для {osname()} завершена.\n")

def osname():
    return "Linux"

def main():
    current_directory = dir()
    current_directory_name = cdn(current_directory)
    print("Hudoliy ResourcePacker GUI builder (Linux for python 12)\n========================================================\n")

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
    cmd("clear")

if __name__ == "__main__":
    cls()
    main()