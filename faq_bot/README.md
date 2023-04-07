## Description

Here is an example of FAQ bot built on DFF, that uses Telegram as its interface.
This bot listens for user questions and finds similar questions in its database by using the `clips/mfaq` model.
It displays found questions as buttons. Upon pressing a button,
the bot sends an answer to the question from the database.

In order for the bot to work, set the bot token via [.env](.env).

An example of bot usage:

![image](https://user-images.githubusercontent.com/61429541/219064505-20e67950-cb88-4cff-afa5-7ce608e1282c.png)

## Testing the bot

To test the bot, run the following command:
```commandline
docker build -t telebot-test --target test .
```

## Running the bot

### With docker-compose

To start the bot via docker-compose, run the following command:
```commandline
docker-compose up
```

### With docker

To start the bot via docker, run the following command:
```commandline
docker build -t telebot-prod --target prod .
docker run --env-file .env telebot-prod
```
