from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
reply_keyboard = [['/yes', '/no']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
current_line = 0
lines = ['Ты видел деву на скале', 'В одежде белой над волнами', 'Когда, бушуя в бурной мгле,',
         'Играло море с берегами,', 'Когда луч молний озарял', 'Ее всечасно блеском алым',
         'И ветер бился и летал', 'С ее летучим покрывалом?', 'Прекрасно море в бурной мгле',
         'И небо в блесках без лазури;', 'Но верь мне: дева на скале',
         'Прекрасней волн, небес и бури.']


def echo(update, context):
    update.message.reply_text(f"Я получил сообщение {update.message.text}")


def start(update, context):
    global current_line
    update.message.reply_text(lines[0], reply_markup=ReplyKeyboardRemove())
    current_line += 1
    return 1


def next_line(update, context):
    global current_line
    answer = update.message.text
    if answer != lines[current_line]:
        update.message.reply_text("нет, не так")
        update.message.reply_text(f"Правильно: {lines[current_line]}. Попробуй повторить.")
        return 1
    if current_line + 1 == len(lines):
        update.message.reply_text("Мы молодцы! Давай повторим!", reply_markup=markup)
        return 2
    update.message.reply_text(lines[current_line + 1])
    current_line += 2
    return 1


def stop(update, context):
    return ConversationHandler.END


def main():
    updater = Updater('1022899407:AAGUFsXx6G4srC2T2mwvajLQHuQeJnJG5mU', use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(entry_points=[CommandHandler('start', start)],
                                       states={1: [MessageHandler(Filters.text, next_line)],
                                               2: [CommandHandler('yes', start),
                                                   CommandHandler('no', stop)]},
                                       fallbacks=[CommandHandler('stop', stop)])
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()