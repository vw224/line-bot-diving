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