Клонирование проекта "Карточки интервального повторения"  в другую папку с проверкой его работоспособности.
1. Клонировать проект командой
   git clone https://github.com/VikaDasha506/Cards_clone
2. Создание вертуального окружения командой
   python -m venv venv
3. Активировать вертульное окружениее:
   Для Windows в Command Prompt:
      venv\Scripts\activate
   Для Windows в PowerShell:
      .\venv\Scripts\Activate.ps1
4. Установить зависимости
    pip install -r requirements.txt
5. В проекте все пароли и ключи спрятаны в файле .env,поэтому в него необходимо вписать свои данные.
   ! Файл (.env) Вам необходимо создать.
   Пример:
   SECRET_KEY=ВВЕДИТЕ_ДЖАНГО_СЕКРЕТНЫЙ_КЛЮЧ
   EMAIL_HOST_PASSWORD=ВВЕДИТЕ_ПАРОЛЬ_ОТ_ПОЧТЫ
   EMAIL_HOST=ВВЕДИТЕ_ХОСТ_ПОЧТЫ
   EMAIL_PORT=ВВЕДИТЕ_ПОРТ_ПОЧТЫ
   EMAIL_HOST_USER=ВВЕДИТЕ_ВАШ_ЕМЕЙЛ
6. Далее необходимо запустить проект командой:
   python manage.py runserver
7. Затем необходимо выполнить миграции:
   python manage.py migrate
8. Запускаем проект снова по команде:
   python manage.py runserver
Проект доступен по локальному адресу:
    http://127.0.0.1:8000/