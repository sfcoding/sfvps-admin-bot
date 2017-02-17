#!/usr/bin/python3


from telegram.ext import Updater
from telegram.ext import CommandHandler
import configparser as cp
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

def echoid(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=str(update.message.chat_id))
 

def get_sys_infos():
    
    return get_memory() +"\n"+ get_disk() + "\n" + get_load()

def get_memory():
    tmp = "Memory Usage:\n"
    tmp += os.popen("memusage").read()
    return tmp

def get_disk():
    tmp = "Disk Usage:\n"
    tmp += os.popen("diskspace").read()
    return tmp

def get_load():
    tmp = "Host Load:\n"
    tmp += os.popen("loadavg").read()
    return tmp

if __name__ == "__main__":


    config = cp.ConfigParser()
    config.read("/root/.tbotrc") 
    bot = telegram.Bot(config['AUTH']['API_TOKEN'])

    commandHandlers = [start,status,mem,disk,load,echoid]

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)


    updater = Updater(bot=bot)

    dispatcher = updater.dispatcher


    for f in commandHandlers:
        dispatcher.add_handler(CommandHandler(f.__name__,f))

    bot.sendMessage(chat_id=config['CHAT_IDS']['IDS'].split(",")[0],text="I am up!")

    updater.start_polling()

    
