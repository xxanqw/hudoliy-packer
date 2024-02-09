![Лого](https://github.com/xxanqw/hudoliy-resourcepack/blob/3e22022f440fbe8a61ce429501d7602c1b17a333/src/logo.png)  
# Програма для пакування!

### Як білдити:
**Windows/Linux**
 - Мати встановлений Python [3.11.6](https://www.python.org/downloads/release/python-3116/#:~:text=Python%20community.-,Files,-Version)
 - Рекомендую використовувати venv
    - Windows:
      ```
      python -m venv .venv
      .venv\Source\Activate.ps1
      ```
    - Linux:
      ```
      python3 -m venv .venv
      source .venv/bin/activate
      ```
 - Встановити залежності
   - Windows `pip install -r build/requirements.pip`
   - Linux: `pip3 install -r build/requirements.pip`
 - Для лінукса встановити `patchelf` та `ccache`
    - Arch: `sudo pacman -S patchelf ccache` або `yay -S patchelf ccache`
    - Debian/Ubuntu: `sudo apt install patchelf ccache`
 - Запустити скрипт
   -  Windows: `python build\build.py`
   -  Linux: `python3 build/build.py`  

**macOS**
 - Мати встановлений Python [3.11.6](https://www.python.org/downloads/release/python-3116/#:~:text=Python%20community.-,Files,-Version)
 - Рекомендую використовувати venv
   - macOS:
     ```
     python3 -m venv .venv
     source .venv/bin/activate
     ```
 - Встановити залежності `pip3 install -r macos/requirements.pip`
 - Запустити скрипт `python3 macos/build.py`
 - Робота програми на макосі: https://youtu.be/EKCVUx3VsZw?si=SyPVWGh9sR2h47Qd
