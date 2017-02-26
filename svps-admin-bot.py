#!/usr/bin/python3

from functools import wraps
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackQueryHandler
import configparser as cp
import telegram
import logging
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import KeyboardButton, ReplyKeyboardMarkup 

# Decorator function to handle authorizations
def need_auth(func):
    @wraps(func)
    def check(bot,update, *args,**kwargs):
        if not update.message.chat_id in wlist :
            return noAuth(bot,update)
        else:
            return func(bot,update)

    return check


# Handles non authorized user requests
def noAuth(bot,update):
    sendmsg(bot,update,"YOU ARE NOT AUTHORIZED!")

def sendmsg(bot,update,msg):
    keyboard = [[KeyboardButton("/disk"),\
    KeyboardButton("/mem")],\
    [KeyboardButton("/load"),\
    KeyboardButton("/recentbcks")]]

    reply_markup = ReplyKeyboardMarkup(keyboard)

    bot.sendMessage(chat_id=update.message.chat_id, text=msg,reply_markup=reply_markup, one_time_keyboard=True)

def start(bot, update):
    sendmsg(bot,update,"I am the new SysAd.. Just ask me!")

@need_auth
def status(bot, update):
    sendmsg(bot,update,get_sys_infos())

@need_auth
def mem(bot, update):
    msg = get_memory()
    sendmsg(bot,update,msg)

@need_auth
def disk(bot, update):
    msg = get_disk()
    sendmsg(bot,update,msg)


@need_auth
def load(bot, update):
    msg = get_load()     
    sendmsg(bot,update,msg)

def echoid(bot, update):
    msg = str(update.message.chat_id)
    sendmsg(bot,update,msg)

@need_auth
def recentbcks(bot, update):
    msg = get_recentbcks()
    sendmsg(bot,update,msg)

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

def get_recentbcks():
    tmp = "Last Backups:\n"
    tmp += os.popen("recentbcks").read()
    return tmp

def button(bot,update):
    query = update.callback_query
    bot.sendMessage(text="Selected option: %s" % query.data,
    chat_id=query.message.chat_id,
    message_id=query.message.message_id)


if __name__ == "__main__":


    config = cp.ConfigParser()
    config.read("/root/.tbotrc") 
    bot = telegram.Bot(config['AUTH']['API_TOKEN'])

    commandHandlers = [start,status,mem,disk,load,echoid,recentbcks]

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

    updater = Updater(bot=bot)

    dispatcher = updater.dispatcher

    for f in commandHandlers:
        dispatcher.add_handler(CommandHandler(f.__name__,f))

    updater.dispatcher.add_handler(CallbackQueryHandler(button))


    wlist = set()

    for wID in config['WHITE_LIST_IDS'].values():
        wlist.add(int(wID))

    print ("[ LOG ] Wlist: "+str(wlist))

    bot.sendMessage(chat_id=config['ADMIN_CHAT_IDS']['IDS'].split(",")[0],text="I am up!")

    print ("[ LOG ] Start Polling")
    updater.start_polling(poll_interval=3,bootstrap_retries=-1)
 
