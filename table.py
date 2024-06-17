from flask import Flask, request, abort
import random
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 設置你的 Channel Access Token 和 Channel Secret
YOUR_CHANNEL_ACCESS_TOKEN = 'Pw49Caccq0S56ZOy71Jf9qhTbvQikZa554GASIto3jCvjmeHSXj8gmLyNcPV2NF/i8PpgULCJ7aKc6CXucM7IoZRaD0a51+ITsEfajOv5RwCfrX323tr5MlJgbTOzRBq5q9YXdhZc6OUX3TZzamOBQdB04t89/1O/w1cDnyilFU='
YOUR_CHANNEL_SECRET = 'f737380ab792c64c93714edd82d711c1'

line_bot_api = LineBotApi(Pw49Caccq0S56ZOy71Jf9qhTbvQikZa554GASIto3jCvjmeHSXj8gmLyNcPV2NF/i8PpgULCJ7aKc6CXucM7IoZRaD0a51+ITsEfajOv5RwCfrX323tr5MlJgbTOzRBq5q9YXdhZc6OUX3TZzamOBQdB04t89/1O/w1cDnyilFU=)
handler = WebhookHandler(f737380ab792c64c93714edd82d711c1)

def generate_question():
    num1 = random.randint(1, 100)
    num2 = random.randint(1, 100)
    answer = num1 + num2
    return num1, num2, answer

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # 當前端點機簽名無效時丟出InvalidSignatureError
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == '加法問題':
        num1, num2, answer = generate_question()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"請回答 {num1} + {num2} = ")
        )
    else:
        try:
            user_answer = int(event.message.text)
            if user_answer == answer:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="你好棒！")
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="哈哈 繼續努力")
                )
        except ValueError:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="請輸入有效的數字")
            )

if __name__ == "__main__":
    app.run()
