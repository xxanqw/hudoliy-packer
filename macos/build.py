from os import system as cmd, getcwd as dir, chdir as cd
from os.path import basename as cdn
from os import chdir as cd
from sys import platform as target
from requests import get as req

def build():
    secret = input("\nСкрипт для макосі, бо вона трішки інакша.\nНатисніть Enter щоб почати збірку...")

    print(f"\nЗбірка для macOS...\n")
    if secret == "":
        cmd("python3 setup.py py2app")
    elif secret == "228":
        cmd("python3 setup.py py2app -A")
    print(f"\nЗбірка для macOS завершена.\nФайл збірки знаходиться в папці dist.\n")
    
def main():
    current_directory = dir()
    current_directory_name = cdn(current_directory)
    print("Hudoliy ResourcePacker GUI builder\n==================================\n")

    expected_directory = "macos"
    if current_directory_name != expected_directory:
        print("Ви запустили скрипт не з тієї папки, в якій він знаходиться.")
        if current_directory_name == "hudoliy-packer":
            input("Оскільки ви знаходитесь в кореневій папці натисніть Enter аби змінити папку на build та запустити скріпт...")
            cd(expected_directory)
            build()
    else:
        build()

def cls():
    if target == "darwin":
        cmd("clear")

if __name__ == "__main__":
    if not target == "darwin":
        print("Цей скрипт призначений для macOS.")
        exit()
    else:
        cls()
        main()