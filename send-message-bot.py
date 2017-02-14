#!/usr/bin/python3

#
#   USAGE: python3 send-message-bot.py message [chat_IDs]
#
#   If chat ids are not provided the the program will
#   try to read them from the config file "/root/.tbotrc"   
#   Telegram API token is loaded from the same file.
#
#   Details about the config file can be found at the bottom of this file.   
#   
#   @Author: Andrea Galloni
#   @E-Mail: andreagalloni92[aaatttt]gmail[doooottt]com
#   @License: No-License and NO WARRANTY.
#
#

import telegram
import sys
import configparser as cp


def main(args):

    config = cp.ConfigParser()
    config.read("/root/.tbotrc")   

    args.reverse()
    msg = args.pop()
        
    if(len(args)==0):
        args = config['CHAT_IDS']['IDS'].split(",")

    bot = telegram.Bot(config['AUTH']['API_TOKEN'])

    for chat_id in args:
        bot.sendMessage(chat_id=int(chat_id),text=msg)

if __name__ == "__main__":

    if (len(sys.argv)<2):
        print ("\n[ERROR] Please at least provide the message to send.")
        print ("\n\tUSAGE: python3 send-message-bot.py message [chat_IDs]")
        exit(1)

    main(sys.argv[1:])


#
#   The configuration file has to be placed at: "/root/.tbotrc"
#   the file have to be compliant to the .ini standard 
#       
#       Semicolons (;) at the beginning of the line indicate a comment.
#
#
#       e.g.: 
#
#           ; this is a config file and this is a comment
#           [AUTH]
#           API_TOKEN:YourBotApiToken 
#       
#           [CHAT_IDS]
#           IDS:273371,5678899
#
#

