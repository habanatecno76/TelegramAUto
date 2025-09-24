class Account:
    def __init__(self, api_id, api_hash, phone_number, groups, mensaje, session_file=None, twofa=None):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.groups = groups
        self.mensaje = mensaje
        self.session_file = session_file or f"sessions/session_{phone_number.strip('+')}"
        self.twofa = twofa
        self._is_authenticated = False  # Estado interno

    @property
    def is_authenticated(self):
        """Verifica si la cuenta está autenticada"""
        return self._is_authenticated

    async def verify_authentication(self):
        """Verifica y actualiza el estado de autenticación"""
        try:
            from telethon import TelegramClient
            client = TelegramClient(self.session_file, self.api_id, self.api_hash)
            await client.connect()
            self._is_authenticated = await client.is_user_authorized()
            await client.disconnect()
            return self._is_authenticated
        except:
            return False