from os.path import exists
from os import makedirs
from datetime import datetime
from random import choice

from pyrogram import Client
from pyrogram.handlers import MessageHandler

from config import api_id, api_hash, log_path, rules_path, ignore_path

class App:
    def __init__(self, api_id, api_hash, rules=[], ignore=[], log_path="./logs"):
        self.rules = rules
        self.ignore = ignore
        self.log_path = log_path
        self.log_name = datetime.now().strftime('%Y-%m-%d %H-%M-%S') + '.txt'
        self.app = Client("account", api_id=api_id, api_hash=api_hash)
        handler = MessageHandler(self.message)
        self.app.add_handler(handler)

    def run(self):
        self.app.run()

    def log(self, text):
        print(text)
        if not exists(self.log_path):
            makedirs(self.log_path)
        with open(f"{self.log_path}/{self.log_name}", "a", encoding="utf-8") as file:
            file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {text}\n")

    async def message(self, client, message):
        self.log(message.chat.id)
        try:
            if message.from_user:
                if message.from_user.id in self.ignore:
                    return
            for rule in self.rules:
                if message.chat.id == int(rule[1]):
                    if rule[0] == "react":
                        await message.react(emoji=choice(rule[2:]))
                    if rule[0] == "answer":
                        await message.reply(" ".join(rule[2:]))
                    if rule[0] == "sticker":
                        await message.reply_sticker(choice(rule[2:]))
        except Exception as ex:
            self.log(f"{ex.__class__.__name__} {ex}")

def get_file(path):
    with open(path, mode="r", encoding="utf-8") as file:
        return file.read().splitlines()

def get_rules():
    return [line.split() for line in get_file(rules_path)]

def get_ignore():
    return [int(n) for n in get_file(ignore_path)]

def main():
    rules = get_rules()
    ignore = get_ignore()
    app = App(api_id, api_hash, rules=rules, ignore=ignore, log_path=log_path)
    app.run()

if __name__ == "__main__":
    main()
