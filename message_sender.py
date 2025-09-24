class MessageSender:
    def __init__(self, telegram_client):
        self.telegram_client = telegram_client

    def format_message(self, message_template, **kwargs):
        return message_template.format(**kwargs)

    def send_message(self, group_id, message):
        self.telegram_client.send_message(group_id, message)

    def schedule_message(self, group_id, message, delay):
        import time
        time.sleep(delay)
        self.send_message(group_id, message)