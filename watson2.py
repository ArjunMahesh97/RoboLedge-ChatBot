from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from ibm_watson import AssistantV1
import json

context = None


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    print('Received /start command')
    update.message.reply_text('Hola!\nI\'m here to help you save some money.\nDo you want to get started? :) ')


def help(bot, update):
    print('Received /help command')
    update.message.reply_text('Help!')


def message(bot, update):
    print('Received an update')
    global context

    conversation = AssistantV1(username=assist_username,  # TODO
                                  password=assist_password,  # TODO
                                  version='2018-02-16')

    # get response from watson
    response = conversation.message(
        workspace_id=workspace_id,  # TODO
        input={'text': update.message.text},
        context=context)
    print(json.dumps(response, indent=2))
    context = response['context']

    # build response
    resp = ''
    for text in response['output']['text']:
        resp += text

    update.message.reply_text(resp)

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(bot_id)  # TODO

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, message))

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
