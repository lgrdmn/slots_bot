from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext, CallbackQueryHandler, PicklePersistence
from slots import creator_db, up_balance, start_values, all_players, game, player_finder, resize_bet


def start(update, context):
    creator_db()
    try:
        buttons = [[KeyboardButton(text='spin 🎰'), KeyboardButton(text='bet 💲')],
                   [KeyboardButton(text='credit 💰'), KeyboardButton(text='set_name')]]
        keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        if player_finder(update.message.chat.id) is not None:
            update.message.reply_text('Добро пожаловать в казино-бота!', reply_markup=keyboard)
            start_values(update.message.chat.id)
    except Exception as error:
        print(error)
        raise KeyboardInterrupt
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
        raise KeyboardInterrupt
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
        raise KeyboardInterrupt
    return HOME


def bet(update, context):
    try:
        keyboard = ReplyKeyboardRemove(True)
        update.message.reply_text(f'Введите желаемый размер ставки!', reply_markup=keyboard)
    except Exception as error:
        print(error)
        raise KeyboardInterrupt
    return BET


def read_bet(update, context):
    bet_size = update.message.text
    result = player_finder(update.message.chat.id)
    player_id = result[0][0]
    player_credit = result[0][1]
    try:
        bet_size = int(bet_size)
    except ValueError:
        update.message.reply_text('Ставка должная быть положительным, целым числом и не может превышать ваш баланс!')
        return BET
    if (bet_size > 0) and (bet_size <= player_credit):
        resize_bet(player_id, bet_size)
        buttons = [[KeyboardButton(text='spin 🎰'), KeyboardButton(text='bet 💲')],
                   [KeyboardButton(text='credit 💰'), KeyboardButton(text='set_name')]]
        keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        update.message.reply_text(f'Вы изменили размер ставки!', reply_markup=keyboard)
        return HOME
    else:
        update.message.reply_text('Ставка должная быть положительным, целым числом и не может превышать ваш баланс!')
        return BET


def default(update, _):
    buttons = [[KeyboardButton(text='spin 🎰'), KeyboardButton(text='bet 💲')],
               [KeyboardButton(text='credit 💰'), KeyboardButton(text='set_name')]]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    update.message.reply_markdown(text='Вы находитесь в Главном меню, готовы попытать удачу? 🍀', reply_markup=keyboard)
    return HOME


bot_persistence = PicklePersistence(filename="persistence_file")

updater = Updater("1462029373:AAExm0dW7OTsyODp4IqA2qgTSkYuHIXaDvg", use_context=True, persistence=bot_persistence)

dispatcher = updater.dispatcher

HOME = 0
BET = 10

conversation = ConversationHandler(
    entry_points=[CommandHandler(command="start", callback=start)],
    states={HOME: [MessageHandler(filters=Filters.regex('spin 🎰'), callback=spin),
                   MessageHandler(filters=Filters.regex('credit 💰'), callback=credit),
                   MessageHandler(filters=Filters.regex('bet 💲'), callback=bet)],
            BET: [MessageHandler(filters=Filters.text, callback=read_bet)]
            },
    fallbacks=[MessageHandler(filters=Filters.text, callback=default)],
    persistent=True, name='slot_bot'
)

dispatcher.add_handler(conversation)

updater.start_polling()
