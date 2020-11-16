from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext, CallbackQueryHandler
from slots import creator_db, up_balance, start_values, all_players, game, player_finder


def start(update, context):
    try:
        buttons = [[KeyboardButton(text='spin 🎰'), KeyboardButton(text='bet 💲')],
                   [KeyboardButton(text='credit 💰'), KeyboardButton(text='set_name')]]
        keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        results = player_finder(update.message.chat.id)
        if update.message.chat.id != results[0][0]:
            update.message.reply_text('Добро пожаловать в казино-бота!', reply_markup=keyboard)
            start_values(update.message.chat.id)
    except Exception as error:
        print(error)
    return HOME


def spin(update, context):
    try:
        buttons = [[KeyboardButton(text='spin 🎰'), KeyboardButton(text='bet 💲')],
                   [KeyboardButton(text='credit 💰'), KeyboardButton(text='set_name')]]
        keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        results = player_finder(update.message.chat.id)
        player_credit = results[0][1]
        if player_credit <= 0:
            update.message.reply_text(f'Пожалуйста пополните баланс!'
                                      f'\nБаланс: {player_credit}'
                                      , reply_markup=keyboard)
        else:
            slot1, slot2, slot3, win_size, player_id, game_credit, bet_size = game(update.message.chat.id)
            update.message.reply_text(f'[{slot1}][{slot2}][{slot3}]'
                                      f'\nВыигрыш: {win_size}'
                                      f'\nБаланс: {game_credit}'
                                      f'\nРазмер ставки: {bet_size}'
                                      , reply_markup=keyboard)
    except Exception as error:
        print(error)
    return HOME


def credit(update, context):
    try:
        buttons = [[KeyboardButton(text='spin 🎰'), KeyboardButton(text='bet 💲')],
                   [KeyboardButton(text='credit 💰'), KeyboardButton(text='set_name')]]
        keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        credit_size, bet_size = up_balance(update.message.chat.id)
        update.message.reply_text(f'Ваш баланс пополнен!'
                                  f'\nБаланс: {credit_size}'
                                  f'\nРазмер ставки: {bet_size}'
                                  , reply_markup=keyboard)
    except Exception as error:
        print(error)
    return HOME


def bet(update, context):
    try:
        buttons = [[KeyboardButton(text='spin 🎰'), KeyboardButton(text='bet 💲')],
                   [KeyboardButton(text='credit 💰'), KeyboardButton(text='set_name')]]
        keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        # keyboard = ReplyKeyboardRemove(True)
        update.message.reply_text(f'Введите желаемый размер ставки!', reply_markup=keyboard)
        print(update.message.text)
    except Exception as error:
        print(error)
    return HOME


def default(update, _):
    buttons = [[KeyboardButton(text='spin 🎰'), KeyboardButton(text='bet 💲')],
               [KeyboardButton(text='credit 💰'), KeyboardButton(text='set_name')]]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    update.message.reply_markdown(text='Вы находитесь в Главном меню, готовы попытать удачу? 🍀', reply_markup=keyboard)
    return HOME


creator_db()

updater = Updater("1462029373:AAExm0dW7OTsyODp4IqA2qgTSkYuHIXaDvg", use_context=True)

dispatcher = updater.dispatcher

HOME = 0

conversation = ConversationHandler(
    entry_points=[CommandHandler(command="start", callback=start)],
    states={HOME: [MessageHandler(filters=Filters.regex('spin 🎰'), callback=spin),
                   MessageHandler(filters=Filters.regex('credit 💰'), callback=credit),
                   MessageHandler(filters=Filters.regex('bet 💲'), callback=bet)]
            },
    fallbacks=[MessageHandler(filters=Filters.text, callback=default)]
)

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(filters=Filters.regex('spin 🎰'), callback=spin))
dispatcher.add_handler(MessageHandler(filters=Filters.regex('credit 💰'), callback=credit))
dispatcher.add_handler(MessageHandler(filters=Filters.regex('bet 💲'), callback=bet))

updater.start_polling()

print(all_players())





