from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from database import db

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    db.add_user(message.from_user.id, message.from_user.full_name)
    await message.answer(f"Hello, {message.from_user.first_name}! Use /help to get help with commands.")

@router.message(Command("anotif"))
async def cmd_anotif(message: types.Message):
    db.set_subscription(message.from_user.id, True)
    await message.answer("🔔 Notifications on.")

@router.message(Command("nanotif"))
async def cmd_nanotif(message: types.Message):
    db.set_subscription(message.from_user.id, False)
    await message.answer("🔕 Notifications off.")

@router.message(Command("fb"))
async def cmd_feedback(message: types.Message, command: CommandObject):
    if not command.args:
        return await message.answer("Please, write a feedback text after /fb")
    
    db.add_feedback(message.from_user.id, message.from_user.full_name, command.args)
    await message.answer("✅ Thanks for your feedback!")

@router.message(Command("repos"))
async def cmd_repos(message: types.Message):
    await message.answer(f"All <b>BMods</b> repositories:\n\n"
        f"Cuprarria - https://github.com/BMods-net/Cuprarria\n"
        f"NMAAA - https://github.com/BMods-net/NMAAA\n",
        parse_mode="HTML")

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(f"<b>Commands for this bot:</b>\n\n"
        f"/start - restart bot\n"
        f"/help - show this menu\n"
        f"/repos - show all <b>BMods</b> mods with link for them.\n"
        f"/fb - give us your feedback about mods and/or this bot. Example: <code>/fb Bot is great!</code>\n"
        f"/anotif - subscribe on notifications in this bot.\n"
        f"/nanotif - unsubscribe on notifications in this bot.\n\n"
        f"NOTE: by defoult notifications are on.",
        parse_mode="HTML")