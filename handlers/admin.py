from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database import db
from states import AdminState
from keyboards import admin_menu
from config import ADMIN_ID, STORAGE_CHANNEL_ID

router = Router()

@router.message(Command("admin"), F.from_user.id == ADMIN_ID)
async def admin_panel(message: Message):
    await message.answer("Admin paneliga xush kelibsiz:", reply_markup=admin_menu())

@router.message(F.text == "➕ Kanal Qo'shish", F.from_user.id == ADMIN_ID)
async def add_channel_start(message: Message, state: FSMContext):
    await message.answer("Kanal ID sini kiriting (masalan: -1001234567890):")
    await state.set_state(AdminState.add_channel_id)

@router.message(AdminState.add_channel_id)
async def add_channel_id(message: Message, state: FSMContext):
    await state.update_data(channel_id=int(message.text))
    await message.answer("Kanal taklif havolasini (invite link) kiriting:")
    await state.set_state(AdminState.add_channel_link)

@router.message(AdminState.add_channel_link)
async def add_channel_link(message: Message, state: FSMContext):
    data = await state.get_data()
    await db.add_channel(data['channel_id'], message.text)
    await state.clear()
    await message.answer("Kanal muvaffaqiyatli qo'shildi!")

@router.message(F.text == "📹 Anime Yuklash", F.from_user.id == ADMIN_ID)
async def add_anime_start(message: Message, state: FSMContext):
    await message.answer("Anime uchun unique kod kiriting (masalan: 105):")
    await state.set_state(AdminState.add_anime_code)

@router.message(AdminState.add_anime_code)
async def add_anime_code(message: Message, state: FSMContext):
    await state.update_data(code=message.text)
    await message.answer("Endi anime videoni yuboring:")
    await state.set_state(AdminState.add_anime_video)

@router.message(AdminState.add_anime_video, F.video)
async def add_anime_video(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    sent_msg = await bot.forward_message(chat_id=STORAGE_CHANNEL_ID, from_chat_id=message.chat.id, message_id=message.message_id)
    await db.add_anime(data['code'], sent_msg.message_id)
    await state.clear()
    await message.answer(f"Anime bazaga saqlandi! KODI: {data['code']}")

@router.message(F.text == "📊 Statistika", F.from_user.id == ADMIN_ID)
async def stats(message: Message):
    data = await db.get_stats()
    await message.answer(f"📊 **Statistika:**\n\nJami foydalanuvchilar: {data['total']}\nFaol foydalanuvchilar: {data['active']}", parse_mode="Markdown")
