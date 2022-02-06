# (c) @AbirHasan2005

import asyncio
from pyrogram import types, errors
from configs import Config
from bot.core.db.database import db


async def show_settings(m: "types.Message"):
    usr_id = m.chat.id
    user_data = await db.get_user_data(usr_id)
    if not user_data:
        await m.edit("Verileriniz Veritabanından Alınamadı!")
        return
    upload_as_doc = user_data.get("upload_as_doc", False)
    caption = user_data.get("caption", None)
    apply_caption = user_data.get("apply_caption", True)
    thumbnail = user_data.get("thumbnail", None)
    buttons_markup = [
        [types.InlineKeyboardButton(f"Dosya Olarak Yükle {'✅' if upload_as_doc else '❌'}",
                                    callback_data="triggerUploadMode")],
        [types.InlineKeyboardButton(f"Altyazı Uygula {'✅' if apply_caption else '❌'}",
                                    callback_data="triggerApplyCaption")],
        [types.InlineKeyboardButton(f"Varsayılan Altyazı Uygula {'❌' if caption else '✅'}",
                                    callback_data="triggerApplyDefaultCaption")],
        [types.InlineKeyboardButton("Özel Altyazı Ayarla",
                                    callback_data="setCustomCaption")],
        [types.InlineKeyboardButton(f"{'Change' if thumbnail else 'Set'} Thumbnail",
                                    callback_data="setThumbnail")]
    ]
    if thumbnail:
        buttons_markup.append([types.InlineKeyboardButton("Kayıtlı Thumbnail Göster",
                                                          callback_data="showThumbnail")])
    if caption:
        buttons_markup.append([types.InlineKeyboardButton("Kayıtlı Altyazı Göster",
                                                          callback_data="showCaption")])
    buttons_markup.append([types.InlineKeyboardButton("Close Message",
                                                      callback_data="closeMessage")])

    try:
        await m.edit(
            text="**Buradan Ayarlarınızı Yapabilirsiniz:**",
            reply_markup=types.InlineKeyboardMarkup(buttons_markup),
            disable_web_page_preview=True,
            parse_mode="Markdown"
        )
    except errors.MessageNotModified: pass
    except errors.FloodWait as e:
        await asyncio.sleep(e.x)
        await show_settings(m)
    except Exception as err:
        Config.LOGGER.getLogger(__name__).error(err)
