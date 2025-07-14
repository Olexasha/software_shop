FROM python:3.12-alpine

RUN apk update && apk add --no-cache \
    bash \
    postgresql-client \
    build-base \
    postgresql-dev \
    libpq

COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

RUN adduser -D -u 1000 main_user

# копируем все файлы корня проекта в корневую одноимённую диреткорию контейнера
# (директория /software_shop создаётся при копировании)
COPY ./ /software_shop
# рабочей директорией делаем ту, где находится manage.py
WORKDIR /software_shop/software_shop
RUN chown -R main_user:main_user /software_shop

USER main_user

EXPOSE 8000

