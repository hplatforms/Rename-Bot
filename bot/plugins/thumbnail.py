# (c) @AbirHasan2005

from bot.client import Client
from pyrogram import filters
from pyrogram import types
from bot.core.db.database import db
from bot.core.db.add import add_user_to_database


@Client.on_message(filters.command("show_thumbnail") & filters.private & ~filters.edited)
async def show_thumbnail(c: Client, m: "types.Message"):
    if not m.from_user:
        return await m.reply_text("Senin Hakkında Bilgim Yok! :(")
    await add_user_to_database(c, m)
    thumbnail = await db.get_thumbnail(m.from_user.id)
    if not thumbnail:
        return await m.reply_text("Thumbnail Ayarlamadınız!")
    await c.send_photo(m.chat.id, thumbnail, caption="Custom Thumbnail",
                       reply_markup=types.InlineKeyboardMarkup(
                           [[types.InlineKeyboardButton("Thumbnail Sil",
                                                        callback_data="deleteThumbnail")]]
                       ))


@Client.on_message(filters.command("set_thumbnail") & filters.private & ~filters.edited)
async def set_thumbnail(c: Client, m: "types.Message"):
    if (not m.reply_to_message) or (not m.reply_to_message.photo):
        return await m.reply_text("Thumbnail Ayarlamak İçin Resim Gönder ve /set_thumbnail Komutuyla Yanıtla!")
    if not m.from_user:
        return await m.reply_text("Senin Hakkında Bilgim Yok! :(")
    await add_user_to_database(c, m)
    await db.set_thumbnail(m.from_user.id, m.reply_to_message.photo.file_id)
    await m.reply_text("Tamam,\n"
                       "Bu Resim Thumbnail Olarak Ayarlandı.",
                       reply_markup=types.InlineKeyboardMarkup(
                           [[types.InlineKeyboardButton("Thumbnail Sil",
                                                        callback_data="deleteThumbnail")]]
                       ))


@Client.on_message(filters.command("delete_thumbnail") & filters.private & ~filters.edited)
async def delete_thumbnail(c: Client, m: "types.Message"):
    if not m.from_user:
        return await m.reply_text("Senin Hakkında Bilgim Yok! :(")
    await add_user_to_database(c, m)
    await db.set_thumbnail(m.from_user.id, None)
    await m.reply_text("Tamam,\n"
                       "Thumbnail Veritabanından Silindi.")
