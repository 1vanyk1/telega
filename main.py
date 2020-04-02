from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
reply_keyboard = [['/lang ru en', '/lang en ru']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
REQUEST_KWARGS = {'proxy_url': 'socks5://173.245.239.12:17145',
                  'urllib3_proxy_kwargs': {'assert_hostname': 'False',
                                           'cert_reqs': 'CERT_NONE'} }


def echo(update, context, user_data):
    update.message.reply_text(f"Я получил сообщение {update.message.text}")


def change_language(update, context, user_data):
    context.user_data['lang'] = f'{context.args[0]}-{context.args[1]}'


def translate(update, context, user_data):
    try:
        if context.user_data['lang'] not in ['ru-en', 'en-ru']:
            context.user_data['lang'] = 'ru-en'
    except BaseException:
          context.user_data['lang'] = 'ru-en'
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


def main():
    updater = Updater(TOKEN, use_context=True, request_kwargs=REQUEST_KWARGS)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("lang", change_language, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, translate, pass_user_data=True))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()