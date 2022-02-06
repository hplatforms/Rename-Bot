# (c) @AbirHasan2005

import asyncio
from bot.client import Client
from bot.core.db.add import (
    add_user_to_database
)
from pyrogram import (
    filters,
    types
)


@Client.on_message((filters.video | filters.audio | filters.document) & ~filters.channel & ~filters.edited)
async def on_media_handler(c: Client, m: "types.Message"):
    if not m.from_user:
        return await m.reply_text("Senin Hakkında Bilgim Yok! :(")
    await add_user_to_database(c, m)
    await asyncio.sleep(3)
    await c.send_flooded_message(
        chat_id=m.chat.id,
        text="**Dosya Bilgilerini Göstermeli miyim?**",
        reply_markup=types.InlineKeyboardMarkup(
            [[types.InlineKeyboardButton("Evet", callback_data="showFileInfo"),
              types.InlineKeyboardButton("Hayır", callback_data="closeMessage")]]
        ),
        disable_web_page_preview=True,
        reply_to_message_id=m.message_id
    )
