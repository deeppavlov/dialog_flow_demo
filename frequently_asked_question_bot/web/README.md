## Description

Example FAQ bot built on `dff` with a web interface.

This example contains a website with a chat interface using `WebSockets`. Chat history is stored inside a `postgresql` database.

The website is accessible via http://localhost:80.

The bot itself works in a following manner:

Whenever a user asks a question it searches for the most similar question in its database using `clips/mfaq` an answer to which is sent to the user.

A showcase of the website:
![faq_web](https://user-images.githubusercontent.com/61429541/233875303-b9bc81c9-522b-4596-8599-6efcfa708d1e.gif)

### Run with Docker & Docker-Compose environment

Build the bot:
```commandline
docker-compose build
```

Running in background
```commandline
docker-compose up -d
```
