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
def message_text(event):
    keyWordWeather = u"天氣"
    #If user don't want to know weather, echo what user input instead.And return t
    if(keyWordWeather not in event.message.text):
       line_bot_api.reply_message(event.reply_token,TextMessage(text=event.message.text))
       return
    #find the location users ask in the string of user input  
    keyWordLocation = u"市縣"
    if event.message.text.find(keyWordLocation[0])>0:
        locationIndex = event.message.text.find(keyWordLocation[0])
    else :
        locationIndex = event.message.text.find(keyWordLocation[1])

    locationIndexStart = locationIndex - 2
    locationIndexEnd = locationIndex + 1
    location = event.message.text[locationIndexStart:locationIndexEnd]
    url="http://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?locationName="+location+"&elementName=Wx"
    header = {"Authorization":os.getenv('APIKEY', None)}
    origin = requests.get(url,headers=header)
    body = json.loads(origin.content)
    #Determind which prediction of time interval for the weather of the location.
    try:
        timeIntervalPredict = body['records']['location'][0]['weatherElement'][0]['time']
        for possibleTime in timeIntervalPredict:
            #type of time info: string -> datetime
            timeInterval = datetime.strptime(possibleTime['startTime'],"%Y-%m-%d %H:%M:%S")
            if(datetime > timeInterval):
                discription = possibleTime['parameter']['paramterName']
        reply= location + u"的天氣為" + discription
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply))
    except:
        line_bot_api.reply_message(event.reply_token,TextMessage(text="yo~台灣沒這個地方～\n或是請愛用繁體「臺」ex「臺南市」"))

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)






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