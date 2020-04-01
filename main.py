from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import json
import random
import copy
reply_keyboard = [['/yes', '/no']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
current_question = 0
questions = json.loads('test.json')["test"]
test = []
ans = [0, 0]


def generate_test():
    global test, current_question
    if len(questions) > 10:
        test = random.sample(questions, 10)
    test = copy.copy(questions)
    random.shuffle(test)
    ans.clear()
    ans.append(0)
    ans.append(0)
    current_question = 0


def echo(update, context):
    update.message.reply_text(f"Я получил сообщение {update.message.text}")


def start(update, context):
    generate_test()
    update.message.reply_text("Здраствуйте! Не хотите пройти опрос?", reply_markup=markup)
    return 1


def start_test(update, context):
    update.message.reply_text(questions[0]['question'])
    return 2


def next_questions(update, context):
    global current_question
    answer = update.message.text
    if answer == questions[current_question]['response']:
        ans[0] = ans[0] + 1
    else:
        ans[1] = ans[1] + 1
    current_question += 1
    if current_question == len(questions):
        update.message.reply_text(f'''Поздравляем! Вы окончили тест! Вы ответили правильно на 
        {ans[0]} вопросов и неправильно на {ans[1]} вопросов''')
        update.message.reply_text('Хотите ещё раз пройти тест?', reply_markup=markup)
        return 1
    else:
        update.message.reply_text(questions[current_question]['question'])
    return 2


def stop(update, context):
    return ConversationHandler.END


def main():
    updater = Updater('1022899407:AAGUFsXx6G4srC2T2mwvajLQHuQeJnJG5mU', use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(entry_points=[CommandHandler('start', start)],
                                       states={1: [CommandHandler('yes', start_test),
                                                   CommandHandler('no', stop)],
                                               2: [MessageHandler(Filters.text, next_questions)]},
                                       fallbacks=[CommandHandler('stop', stop)])
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()