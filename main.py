from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler, ConversationHandler
# REQUEST_KWARGS = {'proxy_url': 'socks5://173.245.239.12:17145',
#                   'urllib3_proxy_kwargs': {'assert_hostname': 'False',
#                                            'cert_reqs': 'CERT_NONE'} }


def echo(update, context):
    update.message.reply_text(f"Я получил сообщение {update.message.text}")


def start(update, context):
    update.message.reply_text("Привет. Пройдите небольшой опрос, пожалуйста!\n"
                              "Вы можете прервать опрос, послав команду /stop.\n"
                              "В каком городе вы живёте?")
    return 1


def first_response(update, context):
    locality = update.message.text
    update.message.reply_text("Какая погода в городе {locality}?".format(**locals()))
    return 2


def second_response(update, context):
    weather = update.message.text
    print(weather)
    update.message.reply_text("Спасибо за участие в опросе! Всего доброго!")
    return ConversationHandler.END


def stop(update, context):
    return ConversationHandler.END


def skip(update, context):
    locality = update.message.text
    update.message.reply_text("Какая погода у вас за окном?")
    return 2


def main():
    updater = Updater('1022899407:AAGUFsXx6G4srC2T2mwvajLQHuQeJnJG5mU', use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(entry_points=[CommandHandler('start', start)],
                                       states={1: [CommandHandler('skip', skip),
                                                   MessageHandler(Filters.text, first_response)],
                                               2: [MessageHandler(Filters.text, second_response)]},
                                       fallbacks=[CommandHandler('stop', stop)])
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()