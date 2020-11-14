from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from slots import creator_db, up_balance, start_values, all_players, game


def start(update, context):
    buttons = [[KeyboardButton(text='spin 🎰'), KeyboardButton(text='bet 💲')],
               [KeyboardButton(text='credit 💰'), KeyboardButton(text='set_name')]]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    update.message.reply_text('Добро пожаловать в казино-бота', reply_markup=keyboard)
    start_values(update.message.chat.id)


def spin(update, context):
    buttons = [[KeyboardButton(text='spin 🎰'), KeyboardButton(text='bet 💲')],
               [KeyboardButton(text='credit 💰'), KeyboardButton(text='set_name')]]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    game(update.message.chat.id)
    slot1, slot2, slot3, win_size, player_id, game_credit, bet_size = game(update.message.chat.id)
    update.message.reply_text(f'[{slot1}][{slot2}][{slot3}]'
                              f'\nВыигрыш: {win_size}'
                              f'\nБаланс: {game_credit}'
                              f'\nРазмер ставки: {bet_size}'
                              , reply_markup=keyboard)


def credit(update, context):
    buttons = [[KeyboardButton(text='spin 🎰'), KeyboardButton(text='bet 💲')],
               [KeyboardButton(text='credit 💰'), KeyboardButton(text='set_name')]]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    up_balance(update.message.chat.id)
    credit_size, bet_size = up_balance(update.message.chat.id)
    update.message.reply_text(f'Ваш баланс пополнен'
                              f'\nБаланс: {credit_size}'
                              f'\nРазмер ставки: {bet_size}'
                              , reply_markup=keyboard)


def main():
    updater = Updater("1462029373:AAExm0dW7OTsyODp4IqA2qgTSkYuHIXaDvg", use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(filters=Filters.regex('spin 🎰'), callback=spin))
    dispatcher.add_handler(MessageHandler(filters=Filters.regex('credit 💰'), callback=credit))

    updater.start_polling()


if __name__ == '__main__':
    creator_db()
    print(all_players())
    main()




