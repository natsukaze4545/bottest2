from flask import Flask, request, abort
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, TemplateSendMessage,ButtonsTemplate,URIAction,
)

import time
import math
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__)

stoptime = 0

stoppoint = 0

setting_ = {
    'use':True,
    'name':'name',
    'point':0,
	'time':0,
	'timepoint':0
}

setting2 = {
	'setting1':False,
	'setting2':False,
	'setting3':False,
	'setting4':False,
	'setting5':False,
	'setting6':False
}
'''
data = {
    'ID':{'name':'point'}
}
'''
def namecheck(ID,name):
    with open('date.json','r') as f:
        date = json.load(f)
    if ID in date:
        if name in date[ID]:
            point = date[ID][name]
            return point
    else:
        data[ID] = {name:0}
        with open('date.json','w') as f:
            json.dump(date, f)
        return 0





#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

class StopWatchTemp(object):
    """
    this can stop counting time temporally.
    """
    def __init__( self, verbose=0) :
        self.make = time.time()
        self.stac = []
        self.stat = "standby"
        self.verbose = verbose
        return

    def start(self) :
        self.stac = []
        self.stat = "running"
        self.st = time.time()
        return self

    def stop(self) :
        (self.stac).append( time.time() - self.st )
        self.stat = "stopped"
        return sum( _ for _ in self.stac )

    def reset(self) :
        self.st = self.make
        self.stat = "standby"
        self.stac = []
        return self

    def restart(self) :
        if   self.stat == "stopped" :
            self.stat = "running"
            self.st = time.time()
        elif self.stat == "standby" :
            if self.verbose >= 2 :
                print("start->stop->restart")
            if self.verbose >= 1 :
                print("regarding 'restart' as 'start'.")
            return self.start()
        elif self.stat == "running" :
            if self.verbose >= 2 :
                print("start->stop->restart")
            if self.verbose >= 1 :
                print("regarding 'restart' as 'reset' and 'start'.")
            return self.reset().start()

    def __str__(self) :
        return str( stop() )

def timecount(secs):
	if secs >= 60:
		minute = secs//60
		if minute < 10:
			str_m = '0{}'.format(str(minute))
		elif minute >= 10:
			str_m = str(minute)
		second = secs-minute*60
		if second < 10:
			str_s = '0{}'.format(str(second))
		elif second >= 10:
			str_s = str(second)
		time_ = '{m}:{s}'.format(m=str_m,s=str_s)
	if secs < 60:
		if secs < 10:
			str_s = '0{}'.format(str(secs))
		elif secs >= 10:
			str_s = str(secs)
		time_ = '00:{}'.format(str_s)
	return time_

@app.route("/")
def hello_world():
    return "hello world!"

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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg_from = event.reply_token
    msg_text = event.message.text
    if msg_text == '設定する':
        line_bot_api.reply_message(msg_from,TextSendMessage(text='まずは貯めるのか使うのかを教えてね！\n貯める or 使う'))
        setting2['setting1'] = True


    if msg_text == '貯める' and setting2['setting1'] == True:
        setting_['use'] = False
        setting2['setting1'] = False
        setting2['setting2'] = True
        line_bot_api.reply_message(msg_from,TextSendMessage(text='OK！貯めるに設定したよ！\n次は行う人の名前を教えてね！(ニックネーム可)\n[打ち方] 名前:"行う人の名前"\n例: たろうくんの場合　名前:たろう'))


    if msg_text == '使う' and setting2['setting1'] == True:
        setting_['use'] = True
        setting2['setting1'] = False
        setting2['setting2'] = True
        line_bot_api.reply_message(msg_from,TextSendMessage(text='OK！使うに設定したよ！\n次は行う人の名前を教えてね！(ニックネーム可)\n[打ち方] 名前:"行う人の名前"\n例: たろうくんの場合　名前:たろう'))


    if '名前' in msg_text and setting2['setting2'] == True:
        setting2['setting2'] = False
        setting2['setting3'] = True
        name = msg_text.replace("名前:","")
        setting_['name'] = name
        point = namecheck(msg_from,name)
        setting_['point'] = point
        if setting_['use'] == False:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='OK！今までの合計ポイントは{}だよ！\n次は1分間に取得するポイント数を設定してね！\n[打ち方] ポイント:"一分当たりの取得ポイント(数字)"\n例: 3ポイントの場合　ポイント:3'.format(point)))
        if setting_['use'] == True:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='OK！今までの合計ポイントは{}だよ！\n次は1分間に消費するポイント数を設定してね！\n[打ち方] ポイント:"一分当たりの消費ポイント(数字)"\n例: 3ポイントの場合　ポイント:3'.format(point)))


    if 'ポイント' in msg_text and setting2['setting3'] == True:
        setting2['setting3'] = False
        setting2['setting4'] = True
        str_timepoint = msg_text.replace("ポイント:","")
        timepoint = int(str_timepoint)
        setting_['timepoint'] = timepoint
        line_bot_api.reply_message(msg_from,TextSendMessage(text='OK！{}ポイントに設定できたよ！\n最後に、何分行うか設定してね！\n[打ち方] 時間:"行う分数(数字)"\n例: 5分の場合　時間:5'.format(timepoint)))


    if '時間' in msg_text and setting2['setting4'] == True:
        setting2['setting4'] = False
        str_time = msg_text.replace("時間:","")
        int_time = int(str_time)
        setting_['time'] = int_time
        if setting_['use'] == False:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='OK！{}分に設定できたよ！\n設定項目\n貯めるか使うか : 貯める\n行う人の名前 : {name}\n今までのポイント : {point}\n一分当たりの獲得ポイント : {timepoint}\n行う時間 : {time_}\n始める場合は スタート と言ってね'.format(name=setting_['name'],point=setting_['point'],timepoint=setting_['timepoint'],time_=setting_['time'])))
        if setting_['use'] == True:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='OK！{}分に設定できたよ！\n設定項目\n貯めるか使うか : 使う\n行う人の名前 : {name}\n今までのポイント : {point}\n一分当たりの消費ポイント : {timepoint}\n行う時間 : {time_}\n始める場合は スタート と言ってね'.format(name=setting_['name'],point=setting_['point'],timepoint=setting_['timepoint'],time_=setting_['time'])))

    if '設定確認' in msg_text:
        if setting_['use'] == False:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='設定項目\n貯めるか使うか : 貯める\n行う人の名前 : {name}\n今までのポイント : {point}\n一分当たりの獲得ポイント : {timepoint}\n行う時間 : {time_}'.format(name=setting_['name'],point=setting_['point'],timepoint=setting_['timepoint'],time_=setting_['time'])))
        if setting_['use'] == True:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='設定項目\n貯めるか使うか : 使う\n行う人の名前 : {name}\n今までのポイント : {point}\n一分当たりの消費ポイント : {timepoint}\n行う時間 : {time_}'.format(name=setting_['name'],point=setting_['point'],timepoint=setting_['timepoint'],time_=setting_['time'])))



if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)