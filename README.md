# Foodgram - "Продуктовый помощник"

Сервис, позволяющий публиковать рецепты, подписыватся на публикации других пользователей,
добавлять понравившиеся рецепты в список "Избранное", а перед походом в магазин скачивать
 сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
Доступен <http://130.193.42.75/admin/>  логин: lisa, пароль: 321321cxz!

## Технологии

Python 3.7

Django 2.2.19

Docker Hub

GitHub Actions

Яндекс.Облако

Continuous Integration

## Как запустить проект

Сделайть fork репозитория <https://github.com/waterdog544/foodgram-project-react>

Клонировать репозитарий

```text
git clone <https://github.com/waterdog544/foodgram-project-react>
```

В Secrets GitHub Actions
<https://github.com/waterdog544/foodgram-project-react/settings/secrets/actions> добавить переменные:

```text
DB_ENGINE=<база данных>
DB_NAME=<имя базы данных>
POSTGRES_USER=<логин пользователя базы данных>
POSTGRES_PASSWORD=<пароль пользователя базы данных>
DB_HOST=<название сервиса (контейнера)>
DB_PORT=<порт для подключения к базе данных>
HOST=<хост сервера>
USER=<логин пользователя на сервере>
SSH_KEY=<приватный ssh-key авторизованный на сервере>
TELEGRAM_TO=<id пользователя telegram>
TELEGRAM_TOKEN=<token telegram бота>
DOCKER_USERNAME=<логин пользователя Docker Hub>
DOCKER_PASSWORD=<пароль пользователя Docker Hub>
```

Запустить сервер

Установить docker и docker-compose на сервере

```text
sudo apt-get update
sudo apt install docker.io
sudo apt-get install docker-compose-plugin
```

Копировать из локальной папки проекта файлы docker-compose.yaml и nginx/default.conf на сервер в home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx/default.conf соответственно

Загрузить проект на git hub в ветку master

```text
git add .
git commit -m 'text'
git push
```

## Алгоритм регистрации пользователей на странице проекта Foodgram

1. Пользователь регистрируется по логину, паролю, email, имени, фамилии
2. Пользователь авторизуется по email  и паролю.
3. Неавторизованные пользователи могут просматривать страницы рецептов и страницы других пользователей.

### Авторы

Шванов Андрей, Yandex Практикум

![This is status](https://github.com/waterdog544/foodgram-project-react/actions/workflows/main.yml/badge.svg?status)
