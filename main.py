import asyncio
import threading
import sys
from test_send_message import publish
from account import Account

# Configuración global
stop_event = threading.Event()
input_lock = threading.Lock()

def load_config():
    """Carga la configuración inicial"""
    try:
        with open('announce.txt', 'r', encoding='utf-8') as file:
            message = file.read()
        
        with open('groups.txt', 'r') as file:
            groups = file.read().split()

        with open('mygroups.txt', 'r') as file:
            mygroups = file.read().split()

        with open('myannounce.txt', 'r', encoding='utf-8') as file:
            mymessage = file.read()  # Cambiado de split() a read()
            
        return message, groups, mymessage, mygroups  # ORDEN CORREGIDO
    except Exception as e:
        print(f"Error cargando configuración: {str(e)}")
        sys.exit(1)

def setup_accounts(message, groups, mymessage, mygroups):  # Parámetros en orden correcto
    """Configura las cuentas a usar"""
    accounts = [
      Account(
            api_id="26085274",
            api_hash="32ca31a8b193d1f30530bb178fc1f649",
            phone_number="+5353579194",
            groups=groups,
            mensaje=message,
            session_file="sessions/session_5353579194",
            twofa=None
        ),
        Account(
            api_id="26690969",
            api_hash="1e4eaea3c0d2c70b7239df59b63e46a2",
            phone_number="+5354380389",
            groups=groups,
            mensaje=message,
            session_file="sessions/session_5354380389",
            twofa=None
        ),
        Account(
            api_id="29137083",
            api_hash="06bbf0804eafb8f3b3d254ac015a3b84",
            phone_number="+5353264164",
            groups=groups,
            mensaje=message,
            session_file="sessions/session_5353264164",
            twofa=None
        ),
        Account(
            api_id="13335642",
            api_hash="e0810121ee36ce9bb5a5162e7db0efa4",
            phone_number="+5363682005",
            groups=groups,
            mensaje=message,
            session_file="sessions/session_5363682005",
            twofa=None
        ),
        Account(
            api_id="27432333",
            api_hash="5005f20d5a48ea9fcd147d3cfcfaa9bc",
            phone_number="+5363983030",
            groups=groups,
            mensaje=message,
            session_file="sessions/session_5363983030",
            twofa=None
        ),
        Account(
            api_id="15549113",
            api_hash="f19e4d8535ec98d0a75152d62dda6412",
            groups=groups,
            phone_number="+5351592941",
            mensaje=mymessage,
            session_file="sessions/session_5351592941",
            twofa=None
        ),
         Account(
            api_id="15549113",
            api_hash="f19e4d8535ec98d0a75152d62dda6412",
            phone_number="+5353332042",
            groups=groups,
            mensaje=message,
            session_file="sessions/session_5353332042",
            twofa=None
        )
    ]
    return accounts

def run_async_publish(account):
    """Wrapper seguro para ejecutar publish en un hilo"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(publish(account))
    except Exception as e:
        print(f"🌀 Error en hilo {account.phone_number}: {str(e)}")
    finally:
        loop.close()

def main_loop(accounts):
    print("\nIniciando todos los bots... (q para detener)")
    threads = []
    for account in accounts:
        t = threading.Thread(
            target=run_async_publish,
            args=(account,),
            daemon=True
        )
        t.start()
        threads.append(t)
        print(f"⚡ Iniciada: {account.phone_number}")
    
    # Esperar finalización
    for t in threads:
        t.join()
        
    print("\nTodos los bots han terminado")
                
if __name__ == "__main__":
    # ORDEN CORREGIDO al recibir los valores de load_config()
    message, groups, mymessage, mygroups = load_config()
    accounts = setup_accounts(message, groups, mymessage, mygroups)
    main_loop(accounts)