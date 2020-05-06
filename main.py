from telegram.ext import Updater, MessageHandler, Filters
import requests


def get_ll_spn(toponym):
    try:
        toponym_coodrinates = ','.join(toponym["Point"]["pos"].split())
    except:
        return ['Ошибка в определении положения']
    try:
        corners = [list(map(float, i.split())) for i in toponym['boundedBy']['Envelope'].values()]
        corners = ','.join([str(corners[1][0] - corners[0][0]), str(corners[1][1] - corners[0][1])])
    except:
        return ['Ошибка в определении размера']
    return [toponym_coodrinates, corners]


def geocoder(update, context):
    geocoder_uri = "http://geocode-maps.yandex.ru/1.x/"
    response = requests.get(geocoder_uri, params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "format": "json",
        "geocode": update.message.text})
    toponym_json = response.json()["response"]["GeoObjectCollection"]["featureMember"]
    if len(toponym_json):
        update.message.reply_text(f"К сожалению не удалось найти {update.message.text}")
    toponym = toponym_json[0]["GeoObject"]
    res = get_ll_spn(toponym)
    if len(res) == 1:
        update.message.reply_text(f"{res[0]} {update.message.text}")
        return
    ll, spn = res[0], res[1]
    static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l=map&pt={ll},org"
    context.bot.send_photo(update.message.chat_id, static_api_request, caption=update.message.text)


def main():
    updater = Updater('1022899407:AAGUFsXx6G4srC2T2mwvajLQHuQeJnJG5mU', use_context=True)
    dp = updater.dispatcher
    text_handler = MessageHandler(Filters.text, geocoder)
    dp.add_handler(text_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()