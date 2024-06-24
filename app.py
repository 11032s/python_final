import os
import sys
import random
import requests
from bs4 import BeautifulSoup
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

def extract_chengyu_from_url(url):
    try:
        # 發送請求到指定網址，並使用utf-8編碼解析
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        response.raise_for_status()  # 確認是否成功取得響應
        response.encoding = 'big5'
        # 使用BeautifulSoup解析HTML，指定from_encoding='utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        # 找到包含成語的所有 <p> 標籤
        p_tags = soup.find_all('p')

        # 過濾包含成語的 <p> 標籤列表
        chengyu_paragraphs = []
        for p_tag in p_tags:
            if '成語：' in p_tag.text:
                chengyu_paragraphs.append(p_tag)
        
        # 從包含成語的標籤中隨機選擇一個
        if chengyu_paragraphs:
            random_p_tag = random.choice(chengyu_paragraphs)
            return random_p_tag.text.strip()  # 返回標籤內文（即包含成語的內容）
        else:
            return None
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching content from {url}: {e}")
        return None
    except Exception as e:
        print(f"Error extracting chengyu: {e}")
        return None

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        # 判斷是否收到 "成語" 文字訊息
        if event.message.text == "成語":
            # 呼叫 extract_chengyu_from_url 函式取得成語
            chengyu = extract_chengyu_from_url('http://w4.hyps.tp.edu.tw/hy164/www/study4.htm')

            if chengyu:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=f"{chengyu}")
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="抱歉，未找到成語。")
                )

    return 'OK'


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
