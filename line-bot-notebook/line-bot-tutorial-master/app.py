from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from bs4 import BeautifulSoup
import requests
app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('lZOvckRIaM/3H2mIrSD2NUsPDOXE+BSARW9kL/73jWbpJzmj5ODO2Wa8s7AmpjafepoxQ9vvsy9ruKcEoKU3tHjFu1ngEjuqycnzwgmxubDNQPWYgDfk6My8NMhBLFdoUwKt3bX9byt3eOzfpV8nDAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('8ec83bc03e710bac6b1209cebe105347')

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'
# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    try:
        compare = ''
        url = 'https://www.etax.nat.gov.tw/etw-main/web/ETW183W1/'
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text,'html.parser')
        data = soup.find_all('tbody')
        table = data[0].find_all('tr')
        latest = table[1].find('a').get('href')
        #print(latest[23])
        for i in range (23,28):
            compare += latest[i]
#==============================================================================
        month = int(text)
        if int(compare) + 1 >= month:
            if month % 2 == 0:
                month -= 1
            path = "https://www.etax.nat.gov.tw/etw-main/web/ETW183W2_"+str(month)
            response = requests.get(path)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text,'html.parser')
            data = soup.find_all('tbody')
            number = data[0].find_all('td',{'class':'number'})
            special = number[0].text
            grand = number[1].text
            first = number[2].text
            addsix = number[3].text
            output = str(int(month/100))+"年"+str(month%100)+'、'+str(month%100 + 1)+"月統一發票\n特別獎:"+special+'\n特獎:'+grand+'\n頭獎:'+first+'\n增開六獎:'+addsix
            message = TextSendMessage(text = output)   
            line_bot_api.reply_message(event.reply_token, message) 
        else:
            message = TextSendMessage(text = 'error') 
            line_bot_api.reply_message(event.reply_token, message)
    except:
        message = TextSendMessage(text = 'error') 
        line_bot_api.reply_message(event.reply_token, message) 
    #message = TextSendMessage(text = '儲存成功')
    #line_bot_api.reply_message(event.reply_token, message)
    
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
