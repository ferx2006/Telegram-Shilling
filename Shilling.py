from telethon.sync import TelegramClient, events
from telethon.tl.types import InputPeerChannel
import os
import asyncio
import config  # Importa el archivo de configuración

print (""""
░▒▓████████▓▒░▒▓████████▓▒░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓████████▓▒░▒▓████████▓▒░░▒▓███████▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
░▒▓██████▓▒░ ░▒▓██████▓▒░ ░▒▓███████▓▒░ ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░  
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓████████▓▒░▒▓████████▓▒░░▒▓██████▓▒░ """)

# Lista de IDs o nombres de usuario de los grupos a los que deseas enviar mensajes
group_ids = ['-4199169250', '@nameofthegroup']  # Utiliza el ID o nombre de usuario del grupo

# Inicializa el cliente de Telegram
session_file = 'telegram_session'

client = TelegramClient(session_file, config.api_id, config.api_hash)

if not client.is_connected():
    client.start(config.phone_number)

async def select_source_group():
    # Obtiene la lista de chats activos
    dialogs = await client.get_dialogs()

    # Filtra los chats para obtener solo los grupos
    groups = [dialog for dialog in dialogs if dialog.is_group]

    # Imprime la lista de grupos
    print("Selecciona un grupo de tus chats activos:")
    for i, group in enumerate(groups, start=1):
        print(f"{i}. {group.name}")

    # Solicita al usuario que elija un grupo
    while True:
        choice = input("Ingresa el número del grupo: ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(groups):
                return groups[index].entity
            else:
                print("Opción inválida. Por favor, intenta nuevamente.")
        except ValueError:
            print("Entrada inválida. Por favor, ingresa un número válido.")

# Variable para almacenar el último mensaje reenviado
last_forwarded_message = None

# Manejador de eventos para nuevos mensajes en el grupo fuente
async def forward_message(event):
    global last_forwarded_message

    # Obtiene el texto del mensaje
    message_text = event.message.text

    # Actualiza el último mensaje reenviado
    last_forwarded_message = message_text

    # Reenvía el mensaje a los grupos especificados
    for group_id in group_ids:
        try:
            # Obtiene la entidad del grupo de destino
            if group_id.startswith('@'):
                target_group_entity = await client.get_entity(group_id)
            else:
                target_group_entity = await client.get_entity(int(group_id))

            # Envía el mensaje al grupo de destino
            await client.send_message(target_group_entity, message_text)
            print(f"Mensaje enviado a {group_id}")
        except ValueError as e:
            print(f"Error: No se pudo encontrar la entidad para el grupo {group_id}. {str(e)}")
        except Exception as e:
            print(f"Error al enviar el mensaje a {group_id}: {str(e)}")

async def resend_last_message():
    while True:
        if last_forwarded_message:
            for group_id in group_ids:
                try:
                    # Obtiene la entidad del grupo de destino
                    if group_id.startswith('@'):
                        target_group_entity = await client.get_entity(group_id)
                    else:
                        target_group_entity = await client.get_entity(int(group_id))

                    # Envía el último mensaje reenviado al grupo de destino
                    await client.send_message(target_group_entity, last_forwarded_message)
                    print(f"Mensaje reenviado a {group_id}")
                except ValueError as e:
                    print(f"Error: No se pudo encontrar la entidad para el grupo {group_id}. {str(e)}")
                except Exception as e:
                    print(f"Error al reenviar el mensaje a {group_id}: {str(e)}")

        # Espera 5 minutos antes de reenviar el mensaje nuevamente
        await asyncio.sleep(300)

async def main():
    # Selecciona el grupo fuente de los chats activos
    source_group_entity = await select_source_group()

    # Registra el manejador de eventos para nuevos mensajes en el grupo fuente seleccionado
    client.add_event_handler(forward_message, events.NewMessage(chats=source_group_entity))

    # Inicia la tarea para reenviar el último mensaje periódicamente
    asyncio.create_task(resend_last_message())

    # Comienza a escuchar nuevos mensajes
    await client.run_until_disconnected()

# Ejecuta el script
with client:
    client.loop.run_until_complete(main())