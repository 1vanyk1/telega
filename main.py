from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import requests
reply_keyboard = [['/lang ru en', '/lang en ru']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
REQUEST_KWARGS = {'proxy_url': 'socks5://173.245.239.12:17145',
                  'urllib3_proxy_kwargs': {'assert_hostname': 'False',
                                           'cert_reqs': 'CERT_NONE'} }


def echo(update, context, user_data):
    update.message.reply_text(f"Я получил сообщение {update.message.text}")


def start(update, context, user_data):
    context.user_data['lang'] = 'ru-en'
    update.message.reply_text("Здраствуйте, я бот-переводчик. Я могу переводить с русского на английский и наоборот. Просто напишите слово, которое нужно перевести.", reply_markup=markup)
    return 1


def change_language(update, context, user_data):
    context.user_data['lang'] = f'{context.args[0]}-{context.args[1]}'


def stop(update, context, user_data):
    return ConversationHandler.END


def translate(update, context, user_data):
    context.user_data['locality'] = update.message.text
    api_server = "https://translate.yandex.net/api/v1.5/tr.json/translate"
    params = {
        "key":
            'trnsl.1.1.20200325T150356Z.9f78a6ddcc4f1fc4.dc324d7ca5564e2f768570df2a4a51690c20377d',
        "text": update.message.text, "lang": context.user_data["lang"]}
    request = requests.get(api_server, params=params)
    try:
        text = str(request.json()['text'])
        update.message.reply_text(text)
    except BaseException:
        update.message.reply_text('Не удалось перевести: ' + update.message.text)
    return 1


def main():
    updater = Updater('1022899407:AAGUFsXx6G4srC2T2mwvajLQHuQeJnJG5mU', use_context=True, request_kwargs=REQUEST_KWARGS)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("lang", change_language))
    conv_handler = ConversationHandler(entry_points=[CommandHandler('start', start,
                                                                    pass_user_data=True)],
                                       states={1: [MessageHandler(Filters.text, translate,
                                                                  pass_user_data=True)]},
                                       fallbacks=[CommandHandler('stop', stop)])
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()