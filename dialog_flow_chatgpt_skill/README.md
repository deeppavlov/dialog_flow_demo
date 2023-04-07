## Description

Here is an example of a customer service bot built on DFF, that uses Telegram as an interface.
This bot is designed to answer any type of user questions in a limited business domain (book shop).

[DNNC](https://github.com/salesforce/DNNC-few-shot-intent) model from Salesforce is used for intent retrieval.
[ChatGPT](https://chat.openai.com/auth/login) is used for generative question answering.

In order for the bot to work, override the stubs in the environment file: [.env](.env).

## DNNC

DNNC model is available at port 4999. 
Service bot interacts with the container via '/respond' endpoint.
The API expects a json object with the dialog history passed as an array and labeled 'dialog_contexts'.
Intents will be extracted from the last utterance.
```json
{
    "dialog_contexts": ["phrase_1", "phrase_2"]
}
```

The API responds with a nested array containing 'label - score' pairs:
```json
[["definition",0.3393537402153015]]
```

## Running the bot

### With docker-compose

To start the bot via docker-compose, run the following command:
```commandline
docker-compose up
```
