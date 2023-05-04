## Description

### Customer service bot

Customer service bot built on `DFF`. Uses telegram as an interface.
This bot is designed to answer any type of user questions in a limited business domain (book shop).

* [DNNC](https://github.com/salesforce/DNNC-few-shot-intent) model ([Zhang et al. 2020](https://arxiv.org/abs/2010.13009)) force is used for intent retrieval.
* [ChatGPT](https://openai.com/pricing#language-models) is used for context based question answering.

### DNNC

DNNC model is available at port 4999. 

Service bot interacts with the container via `/respond` endpoint.
The API expects a json object with the dialog history passed as an array and labeled 'dialog_contexts'. Intents will be extracted from the last utterance.

```json
{
    "dialog_contexts": ["phrase_1", "phrase_2"]
}
```

The API responds with a nested array containing `label - score` pairs.

```json
[["definition",0.3393537402153015]]
```

## Run the bot

### Run with Docker & Docker-Compose environment
In order for the bot to work, set the bot token via [.env](.env.example). You should start by creating your own `.env` file:
```
echo TG_BOT_TOKEN=*** >> .env
echo OPENAI_API_TOKEN=*** >> .env
```

Build the bot:
```commandline
docker-compose build
```
Testing the bot:
```commandline
docker-compose run assistant pytest test.py
```

Running the bot:
```commandline
docker-compose run assistant python run.py
```

Running in background
```commandline
docker-compose up -d
```