from bot.bot import pipeline

if __name__ == "__main__":
    if pipeline.messenger_interface.messenger.token == "":
        raise RuntimeError("Token is not set.")

    pipeline.run()
