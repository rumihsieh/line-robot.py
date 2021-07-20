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

line_bot_api = LineBotApi('rB904vZ3H+XcKag3RMbR1xgtWCWP+8gyCzZRyieo0TkkJMlxy37+bEIw8c9cZGdOD698IOgbSGbY27tMzTbrUrxQL23zTC17lZ0Z4iXedbBwbRZBdi38Ih6A5LHJClvEbkRRdpd1vvvnC2X+Ec8/yAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6fa97fd606b8976830251c314c4f873d')


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