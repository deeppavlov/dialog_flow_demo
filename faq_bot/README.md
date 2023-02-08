## Description

Example FAQ bot built on `dff`. Uses telegram as an interface.

## Testing the bot
```commandline
docker build -t telebot-test --target test .
```

## Running the bot

### With docker

```commandline
docker build -t telebot-prod --target prod .
docker run --env-file .env telebot-prod
```

### With docker-compose

```commandline
docker-compose up
```

## ToDo

1. Remove git installation from Dockerfile when merge/telegram is available via pypi