from dotenv import load_dotenv
from telethon.sync import TelegramClient, events
import os
import json
import asyncio
import re
import unidecode


def normalize_text(text):
    # Elimina caracteres especiales y normaliza a forma NFKD
    text = unidecode.unidecode(text)
    # Mantén solo caracteres alfanuméricos y espacios
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    return text.lower().strip()

async def getListOfGroups(client):
    try:
        dialogs = await client.get_dialogs()
        groups_info = []
        for dialog in dialogs:
            if dialog.is_group or dialog.is_channel:
                entity = await client.get_entity(dialog.id)
                can_send_messages = entity.default_banned_rights is None or not entity.default_banned_rights.send_messages
                if can_send_messages:
                    group_info = {'group_id': dialog.id, 'group_name': dialog.title}
                    groups_info.append(group_info)

        return groups_info
    except Exception as e:
        print(e)
        return []
async def getMessagesFromGroup(client, group_id):
    try:
        all_messages = []
        async for message in client.iter_messages(group_id):
            try:
                all_messages.append(message)
            except:
                pass
        return all_messages
    except Exception as e:
        print(e)
        return []
async def logUserBot():
    load_dotenv()
    api_id = int(26444898)
    api_hash = "1d8f06b8a6616389bf1ffb2f44939b81"
    phone_number = "51962156149"
    session_name = "bot_spammer"
    client = TelegramClient(session_name, api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        await client.sign_in(phone_number, input('Ingrese el código de verificación: '))
    await client.send_message("@spmriverts", f'<b>Bot encendido</b>', parse_mode="HTML")
    spammer_group = int("-4162275385")

    exclude_groups = [
        "Spam 2024", "RESPALDO BINS PERU", "YAPE DE ESTAFADORES", "QUEMANDO ESTAFADORES", 
        "PERU AYUDA", "Referencias Elmer", "CANAL MUNDO STREAMING PERU", "TU MARKETPLACE",
        "REFERENCIAS DE BINS PERU", "RATAS REPORTADAS", "BinsPeru Vip", "Staff bins peru net", 
        "Dox Peru bot", "RESPALDOdeBINS PERU", "YAPE DE ESTAFADORES", "QUEMANDO ESTAFADORES",
        "PERU AYUDA", "Referencias Elmer", "CANAL MUNDO STREAMING PERU", "TU MARKETPLACE"
    ]
    exclude_groups_normalized = [normalize_text(name) for name in exclude_groups]

    while True:
        groups_info = await getListOfGroups(client)
        messages_list = await getMessagesFromGroup(client, spammer_group)
            
        try:
            await client.send_message("@spmriverts", f"<b>CANTIDAD DE MENSAJES CONSEGUIDOS PARA PUBLICAR</b> <code>{len(messages_list)-1}</code>",parse_mode="HTML")
        except:
            pass
            
        try:
            for i in groups_info:
                group_name_normalized = normalize_text(i['group_name'])
                if group_name_normalized not in exclude_groups_normalized:
                # if i['group_name'] not in ["╚»ℝ𝔼𝔽𝔼ℝ𝔼ℕℂ𝕀𝔸𝕊 𝔻𝔼 𝔹𝕀ℕ𝕊_ℙ𝔼ℝ𝕌«╝","─═ＲＡＴＡＳ-ＲＥＰＯＲＴＡＤＡＳ═─","BinsPeru_Vip","Staff bins peru net","Dox_Peru-bot","Spam 2024","RESPALDO🇵🇪BINS PERU","➳𝒀𝑨𝑷𝑬 𝑫𝑬 𝑬𝑺𝑻𝑨𝑭𝑨𝑫𝑶𝑹𝑬𝑺 ✧","QUEMANDO ESTAFADORES","𝐏𝐄𝐑Ú 𝐀𝐘𝐔𝐃𝐀","Referencias Elmer 💸","🎭 CANAL MUNDO STREAMING PERÚ 🇵🇪","TU MARKETPLACE"]:
                    j=0
                    for message_spam in messages_list:
                        j+=1
                        resultado = True
                        try:
                            await client.send_message(i["group_id"], message_spam)
                        except Exception as error:
                            await client.send_message("@spmriverts", f'<b>Error enviando mensajes a {i["group_id"]}</b> - <code>{i["group_name"]}<code>\nCausa:{error}',parse_mode="HTML")
                            resultado = False
                        if resultado:
                            await client.send_message("@spmriverts", f'<b>Mensaje enviado a {i["group_id"]}</b> - <code>{i["group_name"]}</code>',parse_mode="HTML")  
                        await asyncio.sleep(10)
                        if j==1: break
            await client.send_message("@spmriverts", f'<b>RONDA ACABADA</b>', parse_mode="HTML")
            await asyncio.sleep(180) 
        except:
            pass
        
if __name__ == "__main__":
    asyncio.run(logUserBot())