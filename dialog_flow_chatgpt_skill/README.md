## Description

Customer service bot built on `dff`. Uses telegram as an interface.

This bot is designed to answer any type of user questions in a limited business domain (book shop).

[DNNC](#) model from Salesforce is used for intent retrieval.
[ChatGPT](#) is used for generative question answering.

In order for the bot to work, override the stubs in the environment file: [.env](.env).

## Running the bot

### With docker-compose

```commandline
docker-compose up
```
