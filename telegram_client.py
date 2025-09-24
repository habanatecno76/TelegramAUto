from telethon import TelegramClient as TelethonClient

class TelegramClient:
    def __init__(self, api_id, api_hash, phone_number):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.client = TelethonClient(phone_number, api_id, api_hash)

    def login(self):
        self.client.start()

    def send_message(self, group, message):
        if self.client is None:
            raise Exception("Client not logged in. Call login() first.")
        self.client.send_message(group, message)