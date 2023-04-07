## Описание

Представлен пример FAQ-бота, построенного на DFF, использующий в качестве интерфейса Telegram.
Бот получает вопросы от пользователя и находит похожие вопросы в своей базе данных, используя модель `clips/mfaq`.
Найденные вопросы отображаются в виде кнопок. При нажатии на кнопку, бот отправляет ответ на вопрос из базы данных.

Для работы бота установите его токен через [.env](.env).

Пример использования:

![image](https://user-images.githubusercontent.com/61429541/219064505-20e67950-cb88-4cff-afa5-7ce608e1282c.png)

## Тестирование бота

Для тестирования бота, запустите следующую команду:
```commandline
docker build -t telebot-test --target test .
```

## Запуск бота

### Через docker-compose

Чтобы запустить бота через docker-compose, выполните следующую команду:
```commandline
docker-compose up
```

### Через docker

Чтобы запустить бота через docker, выполните следующую команду:
```commandline
docker build -t telebot-prod --target prod .
docker run --env-file .env telebot-prod
```
