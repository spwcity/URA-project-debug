import logging

from aiogram import types, Router, F

import config
from db.User import User
from filters.user import UserAuthFilter

router = Router()


@router.message(F.text.startswith('Я'), UserAuthFilter())
async def send_srat(message: types.Message, user: User):

    must_not_sret = [
        'Я иду срать',
        'Я иду ЛЮТЕЙШЕ ДРИСТАТЬ',
    ]

    must_sret = [
        'Я закончил срать',
    ]

    if message.text in must_sret:
        if not user.sret:
            await message.reply('Ты что заканчивать захотел? Ты даже не срешь!')
            return

    if message.text in must_not_sret:
        if user.sret:
            await message.reply('Ты прошлое свое сранье не закончил, а уже новое начинаешь?\n'
                                'Нет уж. Будь добр, раз начал - закончи.')
            return

    await message.delete()

    if message.text == 'Я иду срать':
        text = '⚠️ *ВНИМАНИЕ* ⚠️\n' \
               '`%s` *прямо сейчас* пошел _срать_'
        sret = True

    elif message.text == 'Я закончил срать':
        text = '⚠️ ВНИМАНИЕ ⚠️\n' \
               '`%s` закончил _срать_'
        sret = False

    elif message.text == 'Я просто пернул':
        text = '⚠️ ВНИМАНИЕ ⚠️\n' \
               '`%s` просто _пернул_'
        sret = False

    elif message.text == 'Я иду ЛЮТЕЙШЕ ДРИСТАТЬ':
        text = '⚠️️️️⚠️⚠️ ВНИМАНИЕ ⚠️⚠️⚠️\n\n' \
               '⚠️НАДВИГАЕТСЯ *ГОВНОПОКАЛИПСИС*⚠️\n' \
               '`%s` *прямо сейчас* пошел _адски дристать_ лютейшей струей *поноса*'
        sret = True

    else:
        return

    user.sret = sret
    user.save()

    for send_to in User.select():
        try:
            await config.Telegram.bot.send_message(send_to.uid, text % message.chat.full_name,
                                                   parse_mode='markdown')

        except Exception as e:
            logging.warning(f'Cannnot send notify to {message.chat.id} cause: {e}')
