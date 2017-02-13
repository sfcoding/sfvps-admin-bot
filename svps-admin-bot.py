from telegram.ext import Updater
from telegram.ext import CommandHandler
import telegram
import logging
import os

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I am the new SysAd.. Just ask me!")

def status(bot, update):
    msg = get_sys_infos()
    bot.sendMessage(chat_id=update.message.chat_id, text=msg)


def mem(bot, update):
    msg = get_memory()
    bot.sendMessage(chat_id=update.message.chat_id, text=msg)

def disk(bot, update):
    msg = get_disk()
    bot.sendMessage(chat_id=update.message.chat_id, text=msg)


def load(bot, update):
    msg = get_load()     
    bot.sendMessage(chat_id=update.message.chat_id, text=msg)

def echo_id(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=str(update.message.chat_id))
 

def get_sys_infos():
    
    return get_memory() +"\n"+ get_disk() + "\n" + get_load()

def get_memory():
    tmp = "Memory Usage:\n"
    tmp += os.popen("/home/andrea/myBins/myScripts/SystemUtils/MemUsage.sh").read()
    return tmp

def get_disk():
    tmp = "Disk Usage:\n"
    tmp += os.popen("/home/andrea/myBins/myScripts/SystemUtils/DiskSpace.sh").read()
    return tmp

def get_load():
    tmp = "Host Load:\n"
    tmp += os.popen("/home/andrea/myBins/myScripts/SystemUtils/LoadAvg.sh").read()
    return tmp

if __name__ == "__main__":

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

    bot = telegram.Bot('372295283:AAHSC3-2zXvlQQx6r7HHVFBkhmdLeFG0-AU')

    updater = Updater(bot=bot) #, token='372295283:AAHSC3-2zXvlQQx6r7HHVFBkhmdLeFG0-AU')

    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)


    status_handler = CommandHandler('status',status)
    dispatcher.add_handler(status_handler)

    mem_status_handler = CommandHandler('mem',mem)
    dispatcher.add_handler(mem_status_handler)

    disk_status_handler = CommandHandler('disk',disk)
    dispatcher.add_handler(disk_status_handler)

    load_status_handler = CommandHandler('load',load)
    dispatcher.add_handler(load_status_handler)
    
    echo_chat_id_handler = CommandHandler('echoid', echo_id)
    dispatcher.add_handler(echo_chat_id_handler) 

    #bot.sendMessage(chat_id=2992341,text="I am up!")

    updater.start_polling()

    
