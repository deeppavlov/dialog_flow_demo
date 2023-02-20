## Description

Example FAQ bot built on `dff`. Uses telegram as an interface.

This bot listens for user questions and finds similar questions in its database by using the `clips/mfaq` model.

It displays found questions as buttons. Upon pressing a button, the bot sends an answer to the question from the database.

In order for the bot to work, set the bot token via [.env](.env).

An example of bot usage:

![image](https://user-images.githubusercontent.com/61429541/219064505-20e67950-cb88-4cff-afa5-7ce608e1282c.png)

## Testing the bot
```commandline
docker build -t telebot-test --target test .
```

## Running the bot

### With docker-compose

```commandline
docker-compose up
```

### With docker

```commandline
docker build -t telebot-prod --target prod .
docker run --env-file .env telebot-prod
```
