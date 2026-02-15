import logging
import configparser

from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

from ChatGPT_HKBU import ChatGPT

gpt = None


async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # await update.message.reply_text(response)
    logging.info("UPDATE: " + str(update))
    loading_message = await update.message.reply_text('Thinking...')

    # send the user message to the ChatGPT client
    response = gpt.submit(update.message.text)

    # send the response to the Telegram box client
    await loading_message.edit_text(response)


def main():
    # Load configuration from ini file
    config = configparser.ConfigParser()
    config.read('config.ini')

    global gpt
    gpt = ChatGPT(config)

    # Create application and add handler
    application = Application.builder().token(config['TELEGRAM']['ACCESS_TOKEN']).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, callback))

    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    main()
