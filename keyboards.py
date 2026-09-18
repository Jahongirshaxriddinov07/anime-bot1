from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔍 Anime Izlash"), KeyboardButton(text="🎲 Tasodifiy Anime")],
            [KeyboardButton(text="⚙️ Shaxsiy Kabinet"), KeyboardButton(text="📢 Anime Kanalimiz")],
            [KeyboardButton(text="🔊 Reklama va Aloqa")]
        ],
        resize_keyboard=True
    )

def admin_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Kanal Qo'shish"), KeyboardButton(text="➖ Kanal O'chirish")],
            [KeyboardButton(text="📹 Anime Yuklash"), KeyboardButton(text="✉️ Xabar Tarqatish")],
            [KeyboardButton(text="📊 Statistika")]
        ],
        resize_keyboard=True
    )

def sub_check_keyboard(channels):
    buttons = []
    for idx, ch in enumerate(channels, 1):
        buttons.append([InlineKeyboardButton(text=f"📢 {idx}-Kanalga obuna bo'ling", url=ch['invite_link'])])
    buttons.append([InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data="check_sub")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
