from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
reply_keyboard1 = [['/room 2', '/exit']]
markup1 = ReplyKeyboardMarkup(reply_keyboard1, one_time_keyboard=False)
reply_keyboard2 = [['/room 3']]
markup2 = ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=False)
reply_keyboard3 = [['/room 4', '/room 1']]
markup3 = ReplyKeyboardMarkup(reply_keyboard3, one_time_keyboard=False)
reply_keyboard4 = [['/room 1']]
markup4 = ReplyKeyboardMarkup(reply_keyboard4, one_time_keyboard=False)
rooms_markups = [markup1, markup2, markup3, markup4]
rooms_info = ['В данном зале представлены статуи римских воинов. Римляни очень ухотели показать свою силу, поэтому воины и война имело одно из важнейших мест в древнеримской культуре.',
              'В данном зале представлены макеты католических церквей. Они выполнены в характерном для Средневековья готическом стиле.',
              'В данном зале представлены картины Леонардо да Винчи и его чертежи. Он был великим учёным, опередившим своё время и жившим в период Возрождения.',
              'В данном зале представлены картины 19 века. На них изображено стремление и желание народа освободиться от влиянии Австрии и Франции и объединиться в одно государство.']


def echo(update, context):
    update.message.reply_text(f"Я получил сообщение {update.message.text}")


def start(update, context):
    update.message.reply_text("Добро пожаловать! Пожалуйста, сдайте верхнюю одежду в гардероб!",
                              reply_markup=markup1)
    return 1


def stop(update, context):
    update.message.reply_text("Всего доброго, не забудьте забрать верхнюю одежду в гардеробе!")
    return ConversationHandler.END


def enter_room(update, context):
    room = int(context.args[0])
    update.message.reply_text(rooms_info[room - 1], reply_markup=rooms_markups[room - 1])
    return room


def main():
    updater = Updater('1022899407:AAGUFsXx6G4srC2T2mwvajLQHuQeJnJG5mU', use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(entry_points=[CommandHandler('start', start)],
                                       states={1: [CommandHandler('room', enter_room)],
                                               2: [CommandHandler('room', enter_room)],
                                               3: [CommandHandler('room', enter_room)],
                                               4: [CommandHandler('room', enter_room)]},
                                       fallbacks=[CommandHandler('exit', stop)])
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()