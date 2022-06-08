до 10.06.22 планируется добавить:
- фильтр публикаций и пользователей в админ-панели
- страницы 404 при попытке окрыть несуществующего пользователя или публикацию
- подправить стиль в некоторых местах
- решить проблему с закончившемся местом на хостинге, от чего он и не работает

**ЗАПУСК ПРОЕКТА НА ЛОКАЛЬНОМ СЕРВЕРЕ (ПК Windows):**
- скачать и разархивировать проект в корень диска С
- скачать и установить язык программирования Python версии 3.9 (включая pip) с официльного сайта.
    <br>скачать: https://www.python.org/downloads/release/python-390/
    <br>как установить: https://python.tutorials24x7.com/blog/how-to-install-python-3-9-on-windows-10
- в командной строке написать:
```
    cd <АДРЕС ПАПКИ "repair_design_fields_DJANGO">
    python -m venv venv
    venv\Scripts\activate
    pip install requirements.txt // установка необходимых плаагинов, а также самого Django
    python manage.py makemigrations
    python manage.py migrate    
    python manage.py runserver    
```
- отрыть информационную систему по адресу 127.0.0.1:8000
- пользоваться, тестировать
