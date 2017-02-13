#!/usr/bin/python3

import telegram
import sys


def main(args):
    args.reverse()
    msg = args.pop()

    bot = telegram.Bot("372295283:AAHSC3-2zXvlQQx6r7HHVFBkhmdLeFG0-AU")
    
    for chat_id in args:
        bot.sendMessage(chat_id=int(chat_id),text=msg)

if __name__ == "__main__":
    main(sys.argv[1:])
