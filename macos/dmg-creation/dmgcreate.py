from os import system as cmd, path as p

# Create a DMG file
def create_dmg():
    cmd('chmod +x create.sh')
    cmd('/bin/bash ./create.sh')

def main():

    cmd('clear')
    print('Створення dmg-файлу для Packer for macOS.')
    print('=========================================\n')
    print('Важливо! Шлях повинен бути абсолютним, та без лапок.\n')
    input(f'Файл збережеться в папці з якої запущений скрипт (Enter для початку)\n')
    create_dmg()

def install_homebrew():
    cmd('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')

def init():
    if not p.exists('/usr/local/bin/brew'):
        print('Homebrew не встановлено.')
        install = input('Встановити Homebrew? (Y/n): ')
        if install == 'Y' or install == 'y' or install == '':
            print('Встановлення Homebrew...')
            install_homebrew()
        else:
            print('Встановлення відмінено.')
            exit()
    if not p.exists('/usr/local/bin/create-dmg'):
        print('create-dmg не встановлено.')
        install = input('Встановити create-dmg? (Y/n): ')
        if install == 'Y' or install == 'y' or install == '':
            print('Встановлення create-dmg...')
            cmd('brew install create-dmg')
        else:
            print('Встановлення відмінено.')
            exit()

if __name__ == '__main__':
    init()
    main()
    print('Готово!')