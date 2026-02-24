from aiogram import Router, F, types
from aiogram.filters import Command, CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config_reader import config
from database import db

router = Router()

@router.message(Command("notify"), F.from_user.id == config.admin_id)
async def cmd_notify(message: types.Message, command: CommandObject):
    if not command.args:
        return await message.answer("Format: /notify Text | Link")

    if "|" in command.args:
        text, url = command.args.split("|", maxsplit=1)
        text, url = text.strip(), url.strip()
    else:
        text, url = command.args.strip(), None

    reply_markup = None
    if url:
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(text="🔗 Download", url=url))
        reply_markup = builder.as_markup()

    users = db.get_subscribed_users()
    
    count = 0
    for user_id in users:
        try:
            await message.bot.send_message(user_id, text, reply_markup=reply_markup, parse_mode="HTML")
            count += 1
        except Exception:
            pass
    
    await message.answer(f"📢 Completed!\n✅Got: {count}")