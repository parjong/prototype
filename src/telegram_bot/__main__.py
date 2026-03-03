
import asyncio
import os

from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters


async def start(update: Update, context) -> None:
    """Sends a message when the command /start is issued."""
    await update.message.reply_text("Hi!")


async def echo(update: Update, context) -> None:
    """Echoes the user's message."""
    print(update.message.text)
    await update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.environ["BOT_TOKEN"]).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
