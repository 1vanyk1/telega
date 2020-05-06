from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import random
reply_keyboard1 = [['/dice', '/timer']]
markup1 = ReplyKeyboardMarkup(reply_keyboard1, one_time_keyboard=False)
reply_keyboard2 = [['/throw 6 1', '/throw 6 2'], ['/throw 20 1', '/close']]
markup2 = ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=False)
reply_keyboard3 = [['/set_timer 30', '/set_timer 60'], ['/set_timer 300', '/close']]
markup3 = ReplyKeyboardMarkup(reply_keyboard3, one_time_keyboard=False)


def dice_menu(update, context):
    update.message.reply_text("Что подбросить?", reply_markup=markup2)


def timer_menu(update, context):
    update.message.reply_text("Какой поставить таймер?", reply_markup=markup3)


def start(update, context):
    update.message.reply_text("Я бот-помочник для настольных игр. Чего изволите?", reply_markup=markup1)


def echo(update, context):
    update.message.reply_text(f"Я получил сообщение {update.message.text}")


def task(context):
    job = context.job
    context.bot.send_message(job.context, text='ВРЕМЯ ИСТЕКЛО!', reply_markup=markup3)


def set_timer(update, context):
    chat_id = update.message.chat_id
    try:
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text('Количество секунд не может быть отрицательным',
                                      reply_markup=markup3)
            return
        if 'job' in context.chat_data:
            old_job = context.chat_data['job']
            old_job.schedule_removal()
        new_job = context.job_queue.run_once(task, due, context=chat_id)
        context.chat_data['job'] = new_job
        update.message.reply_text('Таймер поставлен', reply_markup=markup3)
    except (IndexError, ValueError):
        update.message.reply_text('Использование: /set_timer <секунд>', reply_markup=markup3)


def throw_dice(update, context):
    max = int(context.args[0])
    count = int(context.args[1])
    update.message.reply_text(
        f'Вот результаты: {" ".join(str(random.randint(1, max)) for i in range(count))}',
        reply_markup=markup2)


def unset_timer(update, context):
    if 'job' not in context.chat_data:
        update.message.reply_text('Нет активного таймера')
        return
    job = context.chat_data['job']
    job.schedule_removal()
    del context.chat_data['job']
    update.message.reply_text('Таймер выключен')


def main():
    updater = Updater('1022899407:AAGUFsXx6G4srC2T2mwvajLQHuQeJnJG5mU', use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("dice", dice_menu))
    dp.add_handler(CommandHandler("throw", throw_dice))
    dp.add_handler(CommandHandler("timer", timer_menu))
    text_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("close", start))
    dp.add_handler(CommandHandler("set_timer", set_timer, pass_args=True, pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("unset_timer", unset_timer, pass_chat_data=True))
    dp.add_handler(text_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()