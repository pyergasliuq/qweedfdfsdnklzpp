import os
from aiogram import Bot, types, Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram.enums import ParseMode
from aiogram.types.input_media_document import InputMediaDocument

router = Router()

def search_in_skins(query: str):
    results = []
    try:
        with open('Editing/skins.txt', 'r', encoding='utf-8') as file:
            current_id = None
            current_name = None
            
            for line in file:
                line = line.strip()
                if line.startswith("ID - "):
                    current_id = line[5:]
                elif line.startswith("NAME - "):
                    current_name = line[7:]
                    
                    if current_id and current_name:
                        if query == current_id:
                            return [(current_id, current_name)]
                        
                        clean_query = query.lower().replace('.mod', '')
                        mod_name = current_name.lower().replace('.mod', '')
                        
                        if clean_query in mod_name:
                            results.append((current_id, current_name))
                        
                        current_id = None
                        current_name = None
                    
    except Exception as e:
        print(f"Ошибка: {e}")
        return None
    return results

async def file(id_xyina: str, name_xyina: str, message: Message):
    mod_name = name_xyina.replace('.mod', '').lower()
    
    dff_path = os.path.join('Editing', 'mod', f"{mod_name}.mod")
    dff_file = None
    if os.path.exists(dff_path):
        dff_file = FSInputFile(dff_path)
    
    zip_path = os.path.join('Editing', 'texture', f"texture_{mod_name}.zip")
    zip_file = None
    if os.path.exists(zip_path):
        zip_file = FSInputFile(zip_path)
    
    media_group = []
    text_parts = []
    
    if dff_file:
        media_group.append(InputMediaDocument(media=dff_file))
        text_parts.append(f"{mod_name}.mod")
    
    if zip_file:
        if media_group:
            media_group.append(InputMediaDocument(media=zip_file, caption=f"ID - {id_xyina}\nNAME - {name_xyina}"))
        else:
            media_group.append(InputMediaDocument(media=zip_file, caption=f"ID - {id_xyina}\nNAME - {name_xyina}"))
        text_parts.append(f"texture_{mod_name}.zip")
    
    if media_group:
        await message.answer_media_group(media=media_group)
    
    return text_parts

@router.message(Command("id"))
async def id(message: Message, bot: Bot):
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Чтобы получить и узнать ID, NAME, TEXTURE, MOD файла введите - ID или NAME скина")
        return
    
    query = args[1].strip()
    results = search_in_skins(query)
    
    if results is None:
        await message.answer("Ошибка при чтении файла skins.txt")
    elif not results:
        await message.answer(f"Нет информации о - {query} ID/NAME")
    else:
        id_xyina, name_xyina = results[0]
        
        attached_files = await file(id_xyina, name_xyina, message)
        
        response = []
        if attached_files:
            response.extend(attached_files)
            response.append("")
        response.append(f"ID - {id_xyina}")
        response.append(f"NAME - {name_xyina}")
        
        full_response = "\n".join(response)
        if not attached_files:
            await message.answer(full_response)