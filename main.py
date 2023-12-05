from openai import OpenAI
import os
import credentials
from telegram import Update
from telegram.ext import MessageHandler, CommandHandler, Application, ContextTypes, filters


client = OpenAI(
    api_key= credentials.api_key
)

chat_log = [{"role": "system",
         "content":"You are an intelligent secretary named Bithia"
         }
          ]



BOT_USERNAME = "Bithia_bot"
TOKEN = credentials.bot_api

async def start(update, context):
    await update.message.reply_text("Hello! I am Bithia, your personal assistant😀")

def handle_response(text):
    while True:
        user_message = text
        if user_message.lower() == "quit":
            break
        else:
            chat_log.append({"role":"user", "content":user_message})
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=chat_log
            )
            assistant_response = response.choices[0].message.content
            return assistant_response

async def handle_message(update, context):
    message_type = update.message.chat.type
    text = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type =="group":
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, " ").strip()
            response = handle_response(new_text)
        else:
            return
    else:
        response = handle_response(text)

    print("Bot: ", response)
    await update.message.reply_text(response)

async def error(update, context):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print("starting bot...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=3)