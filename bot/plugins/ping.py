# (c) @AbirHasan2005

from bot.client import Client
from pyrogram import filters
from pyrogram import types
from bot.core.db.add import add_user_to_database


@Client.on_message(filters.command(["start", "ping"]) & filters.private & ~filters.edited)
async def ping_handler(c: Client, m: "types.Message"):
    if not m.from_user:
        return await m.reply_text("Senin Hakkında Bilgim Yok! :(")
    await add_user_to_database(c, m)
    await c.send_flooded_message(
        chat_id=m.chat.id,
        text="Merhaba, Ben Yeniden Alandırma Botuyum!\n\n"
             "Medyayı İndirmeden Yeniden Adlandırabilirim!\n"
             "Hız, Medya DC'nize Bağlıdır.\n\n"
             "Bana Medyayı Gönder ve /rename Komutuyla Cevapla.",
        reply_markup=types.InlineKeyboardMarkup([[
           types.InlineKeyboardButton("Ayarları Göster",
                                      callback_data="showSettings")
        ]])
    )


@Client.on_message(filters.command("help") & filters.private & ~filters.edited)
async def help_handler(c: Client, m: "types.Message"):
    if not m.from_user:
        return await m.reply_text("Senin Hakkında Bilgim Yok! :(")
    await add_user_to_database(c, m)
    await c.send_flooded_message(
        chat_id=m.chat.id,
        text="Medyayı İndirmeden Yeniden Adlandırabilirim!\n"
             "Hız, Medya DC'nize Bağlıdır.\n\n"
             "Bana Medyayı Gönder ve /rename Komutuyla Cevapla.\n\n"
             "Thumbnail Ayarlamak İçin Resim Gönder ve /set_thumbnail Komutuyla Yanıtla\n\n"
             "Ayarlı Thumbnail Görmek İçin /show_thumbnail Komutu Gönder.",
        reply_markup=types.InlineKeyboardMarkup([[
           types.InlineKeyboardButton("Ayarları Göster",
                                      callback_data="showSettings")]])
    )
