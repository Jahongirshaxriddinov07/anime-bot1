from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from database import db
from states import RegistrationState
from keyboards import main_menu, sub_check_keyboard
from config import STORAGE_CHANNEL_ID

router = Router()

async def check_user_subscriptions(bot: Bot, user_id: int) -> bool:
    channels = await db.get_channels()
    for ch in channels:
        try:
            member = await bot.get_chat_member(chat_id=ch['channel_id'], user_id=user_id)
            if member.status in ['left', 'kicked']:
                return False
        except Exception:
            return False
    return True

@router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)
    if not user:
        await message.answer("Assalomu alaykum! Botdan foydalanish uchun ro'yxatdan o'ting.\n\nIsm va familiyangizni kiriting:")
        await state.set_state(RegistrationState.full_name)
    else:
        await check_and_show_menu(message, message.from_user.id)

@router.message(RegistrationState.full_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Yoshingizni kiriting (faqat raqamlarda):")
    await state.set_state(RegistrationState.age)

@router.message(RegistrationState.age)
async def process_age(message: Message, state: FSMContext, bot: Bot):
    if not message.text.isdigit():
        await message.answer("Iltimos, yoshingizni faqat raqamlarda kiriting:")
        return

    data = await state.get_data()
    full_name = data['full_name']
    age = int(message.text)
    user_id = message.from_user.id

    await db.add_user(user_id, full_name, age)
    await state.clear()

    card = f"🆕 **Yangi foydalanuvchi:**\n👤 Ism: {full_name}\n🎂 Yosh: {age}\n🆔 ID: `{user_id}`"
    try:
        await bot.send_message(chat_id=STORAGE_CHANNEL_ID, text=card, parse_mode="Markdown")
    except Exception:
        pass

    await check_and_show_menu(message, user_id)

async def check_and_show_menu(message: Message, user_id: int):
    channels = await db.get_channels()
    if channels:
        is_subbed = await check_user_subscriptions(message.bot, user_id)
        if not is_subbed:
            await message.answer("Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:", reply_markup=sub_check_keyboard(channels))
            return
    await message.answer("Xush kelibsiz! Asosiy menyudan foydalanishingiz mumkin.", reply_markup=main_menu())

@router.callback_query(F.data == "check_sub")
async def check_sub_cb(callback: CallbackQuery, bot: Bot):
    is_subbed = await check_user_subscriptions(bot, callback.from_user.id)
    if is_subbed:
        await callback.message.delete()
        await callback.message.answer("Obuna tasdiqlandi! Asosiy menyu:", reply_markup=main_menu())
    else:
        await callback.answer("Siz hali barcha kanallarga obuna bo'lmadingiz!", show_alert=True)

@router.message(F.text == "🔍 Anime Izlash")
async def search_anime_prompt(message: Message):
    await message.answer("Anime kodini kiriting (masalan: 105):")

@router.message(F.text == "🎲 Tasodifiy Anime")
async def random_anime(message: Message, bot: Bot):
    anime = await db.get_random_anime()
    if anime:
        await bot.copy_message(chat_id=message.from_user.id, from_chat_id=STORAGE_CHANNEL_ID, message_id=anime['message_id'])
    else:
        await message.answer("Bazada hali animelar mavjud emas.")

@router.message(F.text == "⚙️ Shaxsiy Kabinet")
async def profile(message: Message):
    user = await db.get_user(message.from_user.id)
    text = f"⚙️ **Shaxsiy Kabinet**\n\n🆔 ID: `{user['user_id']}`\n👤 Ism: {user['full_name']}\n🎂 Yosh: {user['age']}"
    await message.answer(text, parse_mode="Markdown")

@router.message(F.text.isdigit())
async def get_anime_by_code(message: Message, bot: Bot):
    anime = await db.get_anime(message.text)
    if anime:
        await bot.copy_message(chat_id=message.from_user.id, from_chat_id=STORAGE_CHANNEL_ID, message_id=anime['message_id'])
    else:
        await message.answer("Bunday kodli anime topilmadi.")
