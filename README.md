# Ветеринарная клиника

Веб-приложение «Ветеринарная клиника» на Flask и PostgreSQL.  
Реализована функция «Новый пациент» с возможностью создать, отредактировать и удалить пациента, данные хранятся в PostgreSQL через SQLAlchemy.

---

## Стек

- Python
- Flask
- Flask-SQLAlchemy
- PostgreSQL
- psycopg2-binary

---

## Структура проекта

```text
vet_clinic/
  app/
    __init__.py        # создание Flask-приложения, инициализация БД
    models.py          # ORM-модели (Patient, Doctor, Appointment, MedicalRecord)
    routes.py          # маршруты и обработчики запросов (CRUD пациентов)
    templates/
      base.html
      patients_list.html
      patient_form.html
  db/
    schema.sql         # SQL-схема базы данных
  config.py            # конфигурация приложения
  run.py               # точка входа для запуска приложения
  requirements.txt
  README.md
```

---

## Схема базы данных

Схема описана в `db/schema_db.sql` и содержит таблицы:

- **patients** — пациенты (животные и данные владельца)
- **doctors** — врачи
- **appointments** — записи на приём
- **medical_records** — медицинские записи

Для основной реализованной функции «Новый пациент» используется таблица `patients` и связанные с ней ORM-модели.

---

## Настройка окружения

### 1. Клонировать проект

```bash
git clone <URL_РЕПОЗИТОРИЯ>
cd vet_clinic
```

### 2. Создать виртуальное окружение

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

---

## Настройка PostgreSQL

### 1. Создать базу данных

Предполагается, что у вас установлен PostgreSQL и есть пользователь `postgres` с известным паролем.

Войти в консоль PostgreSQL:

```bash
psql -U postgres
```

Создать базу:

```sql
CREATE DATABASE vet_clinic;
\q
```

### 2. Применить SQL-схему (не обязательно)

Приложение само создаёт таблицы через SQLAlchemy при запуске (`db.create_all()`).  
Дополнительно можно применить `schema.sql` вручную:

```bash
psql -U postgres -d vet_clinic -f db/schema_db.sql
```

---

## Конфигурация подключения к БД

Строка подключения задаётся в `config.py`:

```python
class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:YOUR_PASSWORD@localhost:5432/vet_clinic"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "dev-secret-key"
```

**Необходимо заменить `YOUR_PASSWORD` на реальный пароль пользователя `postgres` в вашей локальной установке PostgreSQL.**

---

## Запуск приложения

В корне проекта:

```bash
source .venv/bin/activate
python3 run.py
```

По умолчанию Flask-сервер поднимается на:

```text
http://127.0.0.1:5000
```

Откройте в браузере, чтобы увидеть список пациентов и редактировать.

---

## Реализованный функционал

### Новый пациент (CRUD)

Маршруты находятся в `app/routes.py`.

Доступные страницы:

- `GET /patients` — список всех пациентов
- `GET /patients/new` — форма создания нового пациента
- `POST /patients/new` — создание пациента в БД
- `GET /patients/<id>/edit` — форма редактирования пациента
- `POST /patients/<id>/edit` — сохранение изменений
- `POST /patients/<id>/delete` — удаление пациента

Все данные сохраняются в таблицу `patients` в базе `vet_clinic` в PostgreSQL через ORM-модель `Patient`.

---

## Как посмотреть данные напрямую в PostgreSQL

```bash
psql -U postgres -d vet_clinic
```

```sql
SELECT * FROM patients;
```

Здесь вы увидите те же записи, которые создавались через веб-интерфейс приложения.

---

## Объектная модель

В `app/models.py` описаны следующие ORM-модели:

- **Patient** — пациенты с полями: `full_name`, `species`, `breed`, `birth_date`, `owner_name`, `owner_phone`
- **Doctor** — врачи с полями: `full_name`, `specialty`
- **Appointment** — записи к врачу с привязкой к пациенту и врачу
- **MedicalRecord** — медицинские записи с диагнозом, лечением и примечаниями

Связи между моделями реализованы через `relationship` и внешние ключи.