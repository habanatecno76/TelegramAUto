import asyncio
import random
import time

import sys
import select

import threading
import os
from telethon import TelegramClient, errors
from telethon.sessions import StringSession

# Variable global para control
stop_sending = False
with open('announcelimited.txt', 'r', encoding='utf-8') as file:
            shorter_message = file.read()

def set_stop_sending():
    global stop_sending
    print("\nPresiona 'q' + Enter para detener...")
    while True:
        # Usa select para lectura no bloqueante
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            if sys.stdin.read(1) == 'q':
                stop_sending = True
                break

async def check_account_authorized(account):
    """Verifica si la cuenta ya está autorizada"""
    client = None
    try:
        client = TelegramClient(
            account.session_file,
            account.api_id,
            account.api_hash
        )
        
        # Conexión sin iniciar sesión para verificar
        await client.connect()
        is_authorized = await client.is_user_authorized()
        return is_authorized
    except Exception as e:
        print(f"⚠ Error verificando autorización: {str(e)}")
        return False
    finally:
        if client and client.is_connected():
            await client.disconnect()

async def login_account(account):
    """Maneja el proceso de login completo"""
    client = None
    try:
        # Verificar si ya está autorizada
        if await check_account_authorized(account):
            print(f"✅ Cuenta {account.phone_number} ya está autorizada")
            return True

        print(f"\n🔐 Iniciando proceso de login para {account.phone_number}")
        
        client = TelegramClient(
            account.session_file,
            account.api_id,
            account.api_hash,
            system_version="4.16.30-vxCustom"
        )

        # Proceso de login interactivo
        await client.start(
            phone=account.phone_number,
            password=account.twofa if account.twofa else None,
            code_callback=lambda: input(f"Introduce el código de verificación para {account.phone_number}: ")
        )

        # Verificación final
        if await client.is_user_authorized():
            print(f"✔ Login exitoso para {account.phone_number}")
            return True
        else:
            print(f"✖ Falló el login para {account.phone_number}")
            return False

    except errors.SessionPasswordNeededError:
        print(f"🔒 La cuenta {account.phone_number} requiere 2FA")
        if account.twofa:
            try:
                await client.start(password=account.twofa)
                return True
            except Exception as e:
                print(f"✖ Error 2FA: {str(e)}")
        else:
            print("✖ No se proporcionó contraseña 2FA")
        return False
    except Exception as e:
        print(f"⚠ Error durante login: {str(e)}")
        return False
    finally:
        if client and client.is_connected():
            await client.disconnect()

async def publish(account):
    global stop_sending
    stop_sending = False

    # Verificar estado de login primero
    if not await login_account(account):
        print(f"⛔ No se puede proceder con {account.phone_number} - Login fallido")
        return

    # Iniciar hilo para escuchar 'q'
    stop_thread = threading.Thread(target=set_stop_sending, daemon=True)
    stop_thread.start()

    client = None
    try:
        client = TelegramClient(
            account.session_file,
            account.api_id,
            account.api_hash,
            connection_retries=3,
            auto_reconnect=True
        )
        await client.connect()

        # Verificación de conexión
        if not client.is_connected():
            raise ConnectionError("No se pudo conectar")

        print(f"\n🚀 Iniciando envíos para {account.phone_number} (q=detener)")

        # Bucle principal de envíos
        while not stop_sending:
            #random.shuffle(account.groups)
            
            for group in account.groups:
                if stop_sending:
                    break

                try:
                    if group == "@MEDICINAS_CUB" or group == "@MEDICINAS_HAB":
                       msg = shorter_message
                    else:
                     msg = f"{account.mensaje}\n\n🟢 {random.choice(['✅', '✨', '⚡'])}"
                    await client.send_message(group, msg)
                    print(f"[{account.phone_number}] ➡ {group}")

                    delay = random.uniform(25, 40)
                    start_time = time.time()
                    while (time.time() - start_time) < delay and not stop_sending:
                        time.sleep(1)

                except errors.FloodWaitError as e:
                    print(f"⏳ Esperando {e.seconds}s (FloodWait)")
                    time.sleep(e.seconds + 5)
                except Exception as e:
                    print(f"⚠ Error enviando mensaje: {str(e)}")
                    time.sleep(10)

    except Exception as e:
        print(f"⚠ Error crítico: {str(e)}")
    finally:
        if client and client.is_connected():
            await client.disconnect()
        print(f"🛑 Sesión finalizada para {account.phone_number}")