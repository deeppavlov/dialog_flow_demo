## Description

Customer service bot built on `dff`. Uses telegram as an interface.

This bot is designed to answer any type of user questions in a limited business domain (book shop).

[DNNC](#) model from Salesforce is used for intent retrieval. Available at port 4999.
[ChatGPT](#) is used for generative question answering.

In order for the bot to work, override the stubs in the environment file: [.env](.env).

## DNNC

DNNC model is available at port 4999. 

Service bot interacts with the container via '/respond' endpoint.
The API expects a json object with the dialog history passed as an array and labeled 'dialog_contexts'. Intents will be extracted from the last utterance.

```json
{
    "dialog_contexts": ["phrase_1", "phrase_2"]
}
```

The API responds with a nested array containing 'label - score' pairs.

```json
[["definition",0.3393537402153015]]
```

## Running the bot

### With docker-compose

```commandline
docker-compose up
```
