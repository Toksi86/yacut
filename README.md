# YaCut - Сервис Укорачивания Ссылки

## Описание Проекта

YaCut - это сервис, позволяющий пользователям сокращать длинные URL-ссылки до более коротких и удобных для использования. Пользователи могут либо предложить свой собственный короткий идентификатор для ссылки, либо сервис автоматически сгенерирует короткую ссылку.

## Как начать работу

### Предварительные требования

- Python 3.8+
- Flask
- SQLAlchemy

### Установка

1. Клонируйте репозиторий:

```
git clone https://github.com/Toksi86/yacut.git
```
2. Перейдите в каталог проекта:

```
cd yacut
```

3. Создайте и активируйте виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

4. Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

5. Создать файл .env по примеру .env_example
```
FLASK_APP=app_name
FLASK_ENV=environment_status
DATABASE_URI=db_info
SECRET_KEY=SecretKey
```

6. Запустите миграции базы данных (если необходимо):

```
flask db upgrade
```

7. Запустите сервер разработки:

```
flask run
```

## Использование

### Интерфейс пользователя

Откройте браузер и перейдите по адресу `http://localhost:5000`. Вы увидите форму для ввода длинной ссылки и необязательного пользовательского короткого идентификатора. После отправки формы, вы получите короткую ссылку, которую можно использовать вместо оригинальной.

### API

#### Создание короткой ссылки

POST-запрос на `http://localhost:5000/api/id/` с JSON-телом, содержащим оригинальную ссылку и необязательным пользовательским идентификатором:

```
json { "original_url": "https://example.com", "custom_id": "optional_custom_id" }
```

#### Получение оригинальной ссылки

GET-запрос на `http://localhost:5000/api/id/<short_id>/`, где `<short_id>` - это короткий идентификатор, полученный после создания короткой ссылки.

## Автор
### *Шперлинг Константин* 