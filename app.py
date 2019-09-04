# wb ↓
import os
import sys
import requests
import simplejson as json
from datetime import datetime
from argparse import ArgumentParser
# wb ↑


from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)


# wb ↓
# get channel_secret and channel_access_token from your enviroment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
assert channel_secret is not None, 'Specify LINE_CHANNEL_SECRET as enviroment variable.'
assert channel_access_token is not None, 'Specify LINE_ACCESS_TOKEN as enviroment variabel.'
# wb ↑

line_bot_api = LineBotApi('P45kdvqNpZchU8nBey8rSHxP7HccFgH43bsRzv+CQ1vPGoC72d3C51XkDFUIbToaYc+pvURu7u/6YHR1mogK3i0ZSsMm6fXJgJFQJYee6RS0tXexfuZ2yOFO7QlQCffIVU0YUa3vD9KeH7m51UO5oAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a1bc96cb9e5e1dba49135aa3acb73803')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    keyWordWeather = u"天氣"   #wb
    if(keyWordWeather not in msg):

        r = '我看不懂你說什麼'

        if msg in ['hi', 'HI', 'Hi']:
            r = '嗨'
        elif msg in ['訂位']:
            r = '您想訂位，是嗎?'

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=r))

        return


if __name__ == "__main__":
    app.run()

git clone https://github.com/Nienzu/LINE-wb-flask
brew cask install ngrok libevent
pip install -r requirements.txt
heroku create 
git add .
git commit -m "Fast Deploy"
git push heroku master

heroku config:set LINE_CHANNEL_SECRET=你LINE的 secret key
heroku config:set LINE_CHANNEL_ACCESS_TOKEN=your-LINE-token
heroku config:set APIKEY=你從中央氣象局拿到的api-key






"""
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('P45kdvqNpZchU8nBey8rSHxP7HccFgH43bsRzv+CQ1vPGoC72d3C51XkDFUIbToaYc+pvURu7u/6YHR1mogK3i0ZSsMm6fXJgJFQJYee6RS0tXexfuZ2yOFO7QlQCffIVU0YUa3vD9KeH7m51UO5oAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a1bc96cb9e5e1dba49135aa3acb73803')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
"""