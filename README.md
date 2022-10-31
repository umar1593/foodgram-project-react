![](https://github.com/umar1593/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
# Foodgram — «Продуктовый помощник»

## Описание проекта Foodgram
«Продуктовый помощник» — Online-сервис на котором пользователи смогут публиковать свои рецепты,
подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное»,
а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или
нескольких выбранных блюд.

Проект можно посмотреть [тут](http://130.193.43.228)


## Реализовано в CI/CD
- автоматический запуск тестов
- обновление образов на Docker Hub
- автоматический деплой на боевой сервер при пуше в главную ветку на гитхабе
- отправка сообщения в Telegram через бота об успешном деплое

## При создании использовано:
- Python 3.7
- Django 3.2.3
- DRF
- Docker
- Docker-Compose
- Nginx
- PostgreSQL
- GitHub Actions

## Запуск проекта на удаленном сервере:
Скачиваем проект с гитхаба:
```
git clone git@github.com:umar1593/foodgram-project-react.git
```
Устанавливаем docker, docker-compose на сервер, затем копируем папку infra на сервер:
```
scp -r infra <username>@<ip>:/home/<username>/
```
Заходим на сервер:
```
ssh <username>@<ip>
```
Переходим в папку infra:
```bash
cd infra
```
Добавляем файл .env в котором хранится SECRET_KEY и настройки БД:
```bash
echo "SECRET_KEY=YourSecretKey 
DB_ENGINE=django.db.backends.postgresql 
DB_NAME=postgres 
POSTGRES_USER=postgres 
POSTGRES_PASSWORD=postgres 
DB_HOST=db DB_PORT=5432" > .env
```
Запускаем проект:
```
sudo docker-compose up -d
```

Выполняем миграции:
```
sudo docker-compose exec backend python manage.py makemigrations
```
```
sudo docker-compose exec backend python manage.py migrate --no-input
```
Создаем суперпользователя:
```
sudo docker-compose exec backend python manage.py createsuperuser
```
Собираем статику:
```
sudo docker-compose exec backend python manage.py collectstatic --no-input
```

Наполняем базу данных ингредиентами и тегами:
```
sudo docker-compose exec backend python manage.py load_tags
```
```
sudo docker-compose exec backend python manage.py load_ingridients
```
### Над проектом работал:  _[< Умар Ширваниев >](https://github.com/umar1593)_
