# Сервис Рассылок

## Описание

Django-приложение для создания и управления email-рассылками.  
Реализованный функционал:

- Авторизация и личный кабинет пользователя
- CRUD-интерфейс для моделей:
  - Клиент
  - Сообщение
  - Рассылка
  - Попытка рассылки
- Привязка объектов к владельцу (`owner`)
- Ограничения по ролям: Менеджер может просматривать всех, остальные — только свои данные
- Кеширование списков и деталки моделей
- Кнопка ручной отправки рассылки
- Команда `send_mails` для отправки активных рассылок по расписанию
- Логирование попыток отправки (`Attempt`)
- Поддержка PostgreSQL, подключение через `.env`
- Интерфейс на русском языке

## Установка

```bash
git clone <ваш-репозиторий>
cd mailing_service
python -m venv .venv
.venv\Scripts\activate  # для Windows
pip install -r requirements.txt
```

Создайте файл `.env`:

```
SECRET_KEY=ваш_секретный_ключ
DEBUG=True
DB_NAME=mailing_service_db
DB_USER=postgres
DB_PASSWORD=ваш_пароль
DB_HOST=localhost
DB_PORT=5432
```

Примените миграции и создайте суперпользователя:

```bash
python manage.py migrate
python manage.py createsuperuser
```

## Запуск

```bash
python manage.py runserver
```

## Дополнительно

- Отправка активных рассылок вручную:

```bash
python manage.py send_mails
```

- Проверка линтером (если установлен `flake8`):

```bash
flake8 --exclude=.venv,migrations
```

## Автор

Проект выполнен в рамках курсовой работы по Django.
