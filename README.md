![Лого](https://github.com/xxanqw/hudoliy-resourcepack/blob/3e22022f440fbe8a61ce429501d7602c1b17a333/src/logo.png)  
# Програма для пакування!

### Як білдити:
Windows/Linux/MacOS
 - Мати встановлений Python [3.11.6](https://www.python.org/downloads/release/python-3116/#:~:text=Python%20community.-,Files,-Version)
 - Рекомендую використовувати venv `python -m venv .venv`
 - Встановити залежності `pip` або `pip3 install -r requirements.pip`
 - Для лінукса встановити `patchelf` та `ccache`
```
   Arch
   sudo pacman -S patchelf ccache
   yay -S patchelf ccache

   Debian/Ubuntu
   sudo apt install patchelf ccache
```
 - Запустити скрипт `python` або `python3 build.py`  
 (ВАЖЛИВО запускати скрипт саме з цієї папки)