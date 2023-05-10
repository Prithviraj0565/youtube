import os

import telegram

from google.oauth2 import service_account

from googleapiclient.discovery import build

from googleapiclient.errors import HttpError

# Initialize the Telegram bot

bot_token = '6166146021:AAGIiEbk75WZDuom3p3CoZYN_NQCdP5H9iU'

bot = telegram.Bot(token=bot_token)

# Initialize the Google API client

creds = service_account.Credentials.from_service_account_file('PATH_TO_YOUR_SERVICE_ACCOUNT_JSON_FILE')

youtube = build('youtube', 'v3', credentials=creds)

# Define a function to handle Telegram messages

def handle_message(update, context):

    message = update.message

    chat_id = message.chat_id

    video_file = message.video.file_id

    video_caption = message.caption

    # Download the video file from Telegram

    video_path = bot.get_file(video_file).download()

    # Upload the video to YouTube

    try:

        request = youtube.videos().insert(

            part="snippet,status",

            body={

                "snippet": {

                    "title": video_caption,

                    "description": video_caption,

                    "tags": ["telegram", "bot"],

                    "categoryId": "22"

                },

                "status": {

                    "privacyStatus": "private"

                }

            },

            media_body=video_path

        )

        response = request.execute()

        video_url = f'https://www.youtube.com/watch?v={response["id"]}'

        bot.send_message(chat_id=chat_id, text=f'Video uploaded to YouTube: {video_url}')

    except HttpError as e:

        bot.send_message(chat_id=chat_id, text=f'Error uploading video to YouTube: {e}')

# Start the Telegram bot

updater = telegram.ext.Updater(token=bot_token, use_context=True)

dispatcher = updater.dispatcher

dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.video, handle_message))

updater.start_polling()

