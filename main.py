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

import psycopg2
import random

from datetime import datetime as dt

def get_connection():
    dsn = os.environ.get('DATABASE_URL')
    return psycopg2.connect(dsn)

'''

conn = get_connection()

cur = conn.cursor()


sql = "insert into retasudb values('user_id','Aくん','100')"

cur.execute("insert into botdb values({id},'{user_id}','{name}','{point}')".format(id=2,user_id='user_id2'+'Aくん2',name='Aくん',point='200'))

cur.execute("UPDATE botdb SET point = '200' WHERE id='2';")

cur.execute("UPDATE botdb SET point = '200' WHERE id='6039';")

cur.execute('SELECT * FROM botdb')



cur = connection.cursor()
cur.execute("ROLLBACK")
conn.commit()

cur.execute('SELECT * FROM botdb')

row_ = []

for row in cur:
    if 'user_id2Aくん' in row:
        ok = row[3]
    else:
        pass
    row_.append(row)

print(ok)

print(row_)


cur.execute("UPDATE botdb SET point = '{point}' WHERE id='{dbID}';".format(point='250',dbID='6039'))


'''


set_ = 2

app = Flask(__name__)

stoptime = 0

stoppoint = 0

setting_ = {}
'''
setting_ = {
    user_id:{
        'use':True,
        'name':'name',
        'point':0,
    	'time':0,
    	'timepoint':0,
        'ID':'',
    }
}
'''
setting2 = {
	'setting1':False,
	'setting2':False,
	'setting3':False,
	'setting4':False,
	'setting5':False,
	'setting6':False,
	'setting7':False,
	'setting8':False,
	'setting9':False,
	'setting10':False,
}



Time = {
    'count':0,
    'pointcount_1':0,
    'pointcount_2':0,
    'pointcount2_1':0,
    'pointcount2_2':0,
}
'''
Time = {
    user_id:{
        'count':0,
        'pointcount_1':0,
        'pointcount_2':0,
        'pointcount2_1':0,
        'pointcount2_2':0
        }
}


date = {
    'ID':{'point':0}
}
'''
date = {}

pdate = {
    'save': True,
    'date': '',
    'point':0
    }
def namecheck(ID,name):
    random_id = random.randint(1,999999)
    point = None
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("ROLLBACK")
    conn.commit()
    cur.execute('SELECT * FROM botdb')
    date[ID] = {'point':0}
    '''
    with open('date.json','r') as f:
        date = json.load(f)
    '''
    for row in cur:
        if ID+name in row:
            str_point = row[3]
            setting_[ID]['dbID'] = row[0]
            date[ID]['point'] = int(str_point)
            return int(str_point)
    '''
    if ID in date:
        if name in date[ID]:
            point = date[ID][name]
            return point
    '''
    if point == None:
        setting_[ID]['dbID'] = random_id
        date[ID]['point'] = 0
        cur.execute("insert into botdb values({id},'{user_id}','{name}','{point}')".format(id=random_id,user_id=ID+name,name=name,point='0'))
        conn.commit()
        return 0


    else:
        setting_[ID]['dbID'] = random_id
        date[ID]['point'] = 0
        cur.execute("insert into botdb values({id},'{user_id}','{name}','{point}')".format(id=random_id,user_id=ID+name,name=name,point='0'))
        conn.commit()
        return 0

def seve(ID):
    try:
        print('ok2')
        print(setting_[ID]['dbID'])
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("ROLLBACK")
        conn.commit()
        cur.execute('SELECT * FROM botdb')
        point = date[ID]['point'] + setting_[ID]['point2']
        str_point = str(point)
        for row in cur:
            if ID+setting_[ID]['name'] in row:
                dbID = row[0]
                print('ok3')
                cur.execute("UPDATE botdb SET point = '{point}' WHERE id='{dbID}';".format(point=str_point,dbID=dbID))
                conn.commit()
                print('ok3-2')
                return
        cur.execute("UPDATE botdb SET point = '{point}' WHERE id='{dbID}';".format(point=str_point,dbID=setting_[ID]['dbID']))
        conn.commit()
        print('ok4')
    except Exception as e:
        print (str(e))
    '''


    with open('date.json','r') as f:
        date = json.load(f)
    date[ID][setting_[ID]['name']] = date[ID][setting_[ID]['name']] + setting_[ID]['point2']
    with open('date.json','w') as f:
        json.dump(date, f)
    '''

def seve2(ID,point):
    try:
        print('ok2')
        print(setting_[ID]['dbID'])
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("ROLLBACK")
        conn.commit()
        cur.execute('SELECT * FROM botdb')
        point_ = namecheck(ID,pdate[ID]['name'])
        point2 = point_ + point
        str_point = str(point2)
        for row in cur:
            if ID+setting_[ID]['name'] in row:
                dbID = row[0]
                print('ok3')
                cur.execute("UPDATE botdb SET point = '{point}' WHERE id='{dbID}';".format(point=str_point,dbID=dbID))
                conn.commit()
                print('ok3-2')
                return
        cur.execute("UPDATE botdb SET point = '{point}' WHERE id='{dbID}';".format(point=str_point,dbID=setting_[ID]['dbID']))
        conn.commit()
        print('ok4')
    except Exception as e:
        print (str(e))

def seve3(ID):
    try:
        tdatetime = dt.now()
        tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
        random_id = random.randint(1,999999)
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("ROLLBACK")
        conn.commit()
        if pdate[ID]['save'] == True:
            date = '追加:'+pdate[ID]['date']
        if pdate[ID]['save'] == False:
            date = '削除:'+pdate[ID]['date']
        cur.execute("insert into botdb values({id},'{user_id}','{date}','{datetime}')".format(id=random_id,user_id=ID+pdate[ID]['name']+'point',date=date,datetime=tstr))
        #cur.execute("insert into botdb values({id},'{user_id}','{date}','{datetime}')".format(id=random_id,user_id=ID+name+'point',date='追加:早起き:10ポイント',datetime='2020-4-14 00:00:00'))
        conn.commit()
    except Exception as e:
        print (str(e))

def pointcheck(ID,name):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("ROLLBACK")
        conn.commit()
        cur.execute('SELECT * FROM botdb')
        date_list = []
        for row in cur:
            if ID+name+'point' in row:
                date = row[2]
                tstr = row[3]
                tdatetime = dt.strptime(tstr, '%Y-%m-%d %H:%M:%S')
                list_ = [date,tdatetime]
                date_list.append(list_)
        d = sorted(date_list, key=lambda s: s[1], reverse=True)
        return d
    except Exception as e:
        print (str(e))


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

s = StopWatchTemp()

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



def count(secs,user_id):
    global set_
    global stoppoint
    for i in range(secs+1, -1, -1):
        if set_ == 1:
            if i == 1:
                print('ok')
                stoppoint = 0
                Time[user_id]['count'] = timecount(i-1)
                if setting_[user_id]['use'] == False:
                    print('1')
                    setting_[user_id]['point2'] = Time[user_id]['pointcount_1']
                    print('2')
                    seve(user_id)
                    print('3')
                    line_bot_api.push_message(setting_[user_id]['ID'],TextSendMessage(text='終了！！\n\n残り時間 : {count}\n経過ポイント : {pointcount_1}\n合計ポイント : {pointcount_2}'.format(count=Time[user_id]['count'],pointcount_1=Time[user_id]['pointcount_1'],pointcount_2=Time[user_id]['pointcount_2'])))
                    print('4')
                if setting_[user_id]['use'] == True:
                    setting_[user_id]['point2'] = Time[user_id]['pointcount2_1']
                    seve(user_id)
                    line_bot_api.push_message(setting_[user_id]['ID'],TextSendMessage(text='終了！！\n\n残り時間 : {count}\n経過ポイント : {pointcount_1}\n合計ポイント : {pointcount_2}'.format(count=Time[user_id]['count'],pointcount_1=Time[user_id]['pointcount2_1'],pointcount_2=Time[user_id]['pointcount2_2'])))
            else:
                Time[user_id]['count'] = timecount(i-1)
                #残り時間
                time.sleep(1)
        else:
            pass


def pointcount(secs,s_point,point,point2,user_id):
    global set_
    global stoppoint
    for i in range(0,secs):
        if set_ == 1:
            Time[user_id]['pointcount_1'] = math.floor(point+i*s_point)
            #経過ポイント
            Time[user_id]['pointcount_2'] = math.floor(point2+point+i*s_point)
            #合計ポイント
            stoppoint = point+i*s_point
            time.sleep(1)
    else:
        pass

def pointcount2(secs,s_point,point,point2,user_id):
	global set_
	global stoppoint
	for i in range(0,secs):
		if set_ == 1:
			Time[user_id]['pointcount2_1'] = math.floor(0-(point+i*s_point))
			Time[user_id]['pointcount2_2'] = math.floor(point2-(point+i*s_point))
			stoppoint = point+i*s_point
			time.sleep(1)
		else:
			pass

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
    global set_
    global stoptime
    global stoppoint
    msg_from = event.reply_token
    msg_text = event.message.text
    user_id = event.source.user_id
    if msg_text == '設定する':
        line_bot_api.reply_message(msg_from,TextSendMessage(text='まずは貯めるのか使うのかを教えてね！\n貯める or 使う'))
        setting_[user_id] = {'use':True,'name':'name','point':0,'time':0,'timepoint':0,'ID':'','point2':0,'dbID':0}
        setting_[user_id]['ID'] = user_id
        Time[user_id] = {'count':0,'pointcount_1':0,'pointcount_2':0,'pointcount2_1':0,'pointcount2_2':0}
        setting2[user_id] = {'setting1':False,'setting2':False,'setting3':False,'setting4':False,'setting5':False,'setting6':False,'setting7':False,'setting8':False,'setting9':False,'setting10':False,}
        set_ = 2

        stoptime = 0

        stoppoint = 0
        setting2[user_id]['setting1'] = True


    if msg_text == '貯める' and setting2[user_id]['setting1'] == True and user_id == setting_[user_id]['ID']:
        setting_[user_id]['use'] = False
        setting2[user_id]['setting1'] = False
        setting2[user_id]['setting2'] = True
        line_bot_api.reply_message(msg_from,TextSendMessage(text='OK！貯めるに設定したよ！\n次は行う人の名前を教えてね！(ニックネーム可)\n[打ち方] 名前:"行う人の名前"\n例: たろうくんの場合　名前:たろう'))


    if msg_text == '使う' and setting2[user_id]['setting1'] == True and user_id == setting_[user_id]['ID']:
        setting_[user_id]['use'] = True
        setting2[user_id]['setting1'] = False
        setting2[user_id]['setting2'] = True
        line_bot_api.reply_message(msg_from,TextSendMessage(text='OK！使うに設定したよ！\n次は行う人の名前を教えてね！(ニックネーム可)\n[打ち方] 名前:"行う人の名前"\n例: たろうくんの場合　名前:たろう'))


    if '名前' in msg_text and setting2[user_id]['setting2'] == True and user_id == setting_[user_id]['ID']:
        setting2[user_id]['setting2'] = False
        setting2[user_id]['setting3'] = True
        name = msg_text.replace("名前:","")
        setting_[user_id]['name'] = name
        point = namecheck(user_id,name)
        setting_[user_id]['point'] = point
        if setting_[user_id]['use'] == False:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='OK！今までの合計ポイントは{}だよ！\n次は1分間に取得するポイント数を設定してね！\n[打ち方] ポイント:"一分当たりの取得ポイント(数字)"\n例: 3ポイントの場合　ポイント:3'.format(point)))
        if setting_[user_id]['use'] == True:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='OK！今までの合計ポイントは{}だよ！\n次は1分間に消費するポイント数を設定してね！\n[打ち方] ポイント:"一分当たりの消費ポイント(数字)"\n例: 3ポイントの場合　ポイント:3'.format(point)))


    if 'ポイント:' in msg_text and setting2[user_id]['setting3'] == True and user_id == setting_[user_id]['ID']:
        setting2[user_id]['setting3'] = False
        setting2[user_id]['setting4'] = True
        str_timepoint = msg_text.replace("ポイント:","")
        timepoint = int(str_timepoint)
        setting_[user_id]['timepoint'] = timepoint
        line_bot_api.reply_message(msg_from,TextSendMessage(text='OK！{}ポイントに設定できたよ！\n最後に、何分行うか設定してね！\n[打ち方] 時間:"行う分数(数字)"\n例: 5分の場合　時間:5'.format(timepoint)))


    if '時間' in msg_text and setting2[user_id]['setting4'] == True and user_id == setting_[user_id]['ID']:
        setting2[user_id]['setting4'] = False
        str_time = msg_text.replace("時間:","")
        int_time = int(str_time)
        setting_[user_id]['time'] = int_time
        if setting_[user_id]['use'] == False:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='OK！{_time}分に設定できたよ！\n設定項目\n貯めるか使うか : 貯める\n行う人の名前 : {name}\n今までのポイント : {point}\n一分当たりの獲得ポイント : {timepoint}\n行う時間 : {time_}\n始める場合は スタート と言ってね'.format(_time=int_time,name=setting_[user_id]['name'],point=setting_[user_id]['point'],timepoint=setting_[user_id]['timepoint'],time_=setting_[user_id]['time'])))
        if setting_[user_id]['use'] == True:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='OK！{_time}分に設定できたよ！\n設定項目\n貯めるか使うか : 使う\n行う人の名前 : {name}\n今までのポイント : {point}\n一分当たりの消費ポイント : {timepoint}\n行う時間 : {time_}\n始める場合は スタート と言ってね'.format(_time=int_time,name=setting_[user_id]['name'],point=setting_[user_id]['point'],timepoint=setting_[user_id]['timepoint'],time_=setting_[user_id]['time'])))

    if '設定確認' in msg_text:
        if setting_[user_id]['use'] == False:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='設定項目\n貯めるか使うか : 貯める\n行う人の名前 : {name}\n今までのポイント : {point}\n一分当たりの獲得ポイント : {timepoint}\n行う時間 : {time_}'.format(name=setting_[user_id]['name'],point=setting_[user_id]['point'],timepoint=setting_[user_id]['timepoint'],time_=setting_[user_id]['time'])))
        if setting_[user_id]['use'] == True:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='設定項目\n貯めるか使うか : 使う\n行う人の名前 : {name}\n今までのポイント : {point}\n一分当たりの消費ポイント : {timepoint}\n行う時間 : {time_}'.format(name=setting_[user_id]['name'],point=setting_[user_id]['point'],timepoint=setting_[user_id]['timepoint'],time_=setting_[user_id]['time'])))

    if 'スタート' == msg_text:
        s_point = round(setting_[user_id]['timepoint']/60,2)
        if set_ == 1 or set_ == 2:
            set_ = 1
            secs = setting_[user_id]['time']*60
            s.start()
            executer = ThreadPoolExecutor(1)
            executer.submit(count, secs, user_id)
            if setting_[user_id]['use'] == False:
                executer = ThreadPoolExecutor(1)
                executer.submit(pointcount, secs,s_point,stoppoint,setting_[user_id]['point'],user_id)
            if setting_[user_id]['use'] == True:
                executer = ThreadPoolExecutor(1)
                executer.submit(pointcount2, secs,s_point,stoppoint,setting_[user_id]['point'],user_id)
       	elif set_ == 0:
            set_ = 1
            secs = setting_[user_id]['time']*60-stoptime
            s.restart()
            executer = ThreadPoolExecutor(1)
            executer.submit(count, secs, user_id)
            if setting_[user_id]['use'] == False:
                executer = ThreadPoolExecutor(1)
                executer.submit(pointcount, secs,s_point,stoppoint,setting_[user_id]['point'],user_id)
            if setting_[user_id]['use'] == True:
                executer = ThreadPoolExecutor(1)
                executer.submit(pointcount2, secs,s_point,stoppoint,setting_[user_id]['point'],user_id)
        line_bot_api.reply_message(msg_from,TextSendMessage(text='スタートしたよ！\n一時停止したいときは ストップ と言ってね！\n確認 で進行状況が確認できるよ！'))


    if 'ストップ' == msg_text:
        if set_ == 1:
        	t1 = s.stop()
        	set_ = 0
        	stoptime = math.floor(t1)
        if setting_[user_id]['use'] == False:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='スタート で再スタートできるよ！\n残り時間 : {count}\n経過ポイント : {pointcount_1}\n合計ポイント : {pointcount_2}'.format(count=Time[user_id]['count'],pointcount_1=Time[user_id]['pointcount_1'],pointcount_2=Time[user_id]['pointcount_2'])))
            setting_[user_id]['point2'] = Time[user_id]['pointcount_1']
        if setting_[user_id]['use'] == True:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='スタート で再スタートできるよ！\n残り時間 : {count}\n経過ポイント : {pointcount_1}\n合計ポイント : {pointcount_2}'.format(count=Time[user_id]['count'],pointcount_1=Time[user_id]['pointcount2_1'],pointcount_2=Time[user_id]['pointcount2_2'])))
            setting_[user_id]['point2'] = Time[user_id]['pointcount2_1']

    if '確認' == msg_text:
        if setting_[user_id]['use'] == False:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='残り時間 : {count}\n経過ポイント : {pointcount_1}\n合計ポイント : {pointcount_2}'.format(count=Time[user_id]['count'],pointcount_1=Time[user_id]['pointcount_1'],pointcount_2=Time[user_id]['pointcount_2'])))
            setting_[user_id]['point2'] = Time[user_id]['pointcount_1']
        if setting_[user_id]['use'] == True:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='残り時間 : {count}\n経過ポイント : {pointcount_1}\n合計ポイント : {pointcount_2}'.format(count=Time[user_id]['count'],pointcount_1=Time[user_id]['pointcount2_1'],pointcount_2=Time[user_id]['pointcount2_2'])))
            setting_[user_id]['point2'] = Time[user_id]['pointcount2_1']


    if 'ポイント追加' == msg_text:
        setting_[user_id] = {'use':True,'name':'name','point':0,'time':0,'timepoint':0,'ID':'','point2':0,'dbID':0}
        setting2[user_id] = {'setting1':False,'setting2':False,'setting3':False,'setting4':False,'setting5':False,'setting6':False,'setting7':False,'setting8':False,'setting9':False,'setting10':False,}
        line_bot_api.reply_message(msg_from,TextSendMessage(text='まずはやったひとの名前を教えてね！\n[打ち方]　やったひと:"名前"\n例: たろうくんの場合  やったひと:たろう'))
        setting2[user_id]['setting9'] = True
        pdate[user_id] = {'save': True,'date': '','point':'','name':''}


    if 'ポイント削除' == msg_text:
        setting_[user_id] = {'use':True,'name':'name','point':0,'time':0,'timepoint':0,'ID':'','point2':0,'dbID':0}
        setting2[user_id] = {'setting1':False,'setting2':False,'setting3':False,'setting4':False,'setting5':False,'setting6':False,'setting7':False,'setting8':False,'setting9':False,'setting10':False,}
        line_bot_api.reply_message(msg_from,TextSendMessage(text='まずはやったひとの名前を教えてね！\n[打ち方]　やったひと:"名前"\n例: たろうくんの場合  やったひと:たろう'))
        setting2[user_id]['setting10'] = True
        pdate[user_id] = {'save': False,'date': '','point':'','name':''}

    if 'やったひと' in msg_text:
        date = msg_text.replace("やったひと:","")
        if setting2[user_id]['setting9'] == True:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='{date}さんがしたんだね！\n\n次はやったことを教えてね！\n[打ち方]　やったこと:"やったこと"\n例:  早起きムした場合  やったこと:早起き'.format(date=date)))
            pdate[user_id]['name'] = date
            setting2[user_id]['setting9'] = False
            setting2[user_id]['setting5'] = True
        if setting2[user_id]['setting10'] == True:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='{date}さんがしたんだね！\n\n次はやったことを教えてね！\n[打ち方]　やったこと:"やったこと"\n例:  ゲームした場合  やったこと:ゲーム'.format(date=date)))
            pdate[user_id]['name'] = date
            setting2[user_id]['setting10'] = False
            setting2[user_id]['setting6'] = True


    if 'やったこと' in msg_text:
        date = msg_text.replace("やったこと:","")
        if setting2[user_id]['setting5'] == True:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='{date}をしたんだね！\n\n次は追加するポイントを教えてね！\n[打ち方]　ポイント:"ポイント数(数字)"\n例: 10ポイントの場合  ポイント:10'.format(date=date)))
            pdate[user_id]['date'] = date
            setting2[user_id]['setting5'] = False
            setting2[user_id]['setting7'] = True
        if setting2[user_id]['setting6'] == True:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='{date}をしたんだね！\n\n次は削除するポイントを教えてね！\n[打ち方]　ポイント:"ポイント数(数字)"\n例: 10ポイントの場合  ポイント:10'.format(date=date)))
            pdate[user_id]['date'] = date
            setting2[user_id]['setting6'] = False
            setting2[user_id]['setting8'] = True

    if 'ポイント' in msg_text:
        point = msg_text.replace("ポイント:","")
        if setting2[user_id]['setting7'] == True:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='{date}をしたから{point}追加されたよ！\n\n今までの記録は  記録確認  で見れるよ！'.format(date=pdate[user_id]['date'],point=point)))
            pdate[user_id]['point'] = point
            setting2[user_id]['setting7'] = False
            seve2(user_id,int(point))
            seve3(user_id)
        if setting2[user_id]['setting8'] == True:
            line_bot_api.reply_message(msg_from,TextSendMessage(text='{date}をしたから{point}削除したよ！\n\n今までの記録は  記録確認  で見れるよ！'.format(date=pdate[user_id]['date'],point=point)))
            setting2[user_id]['setting8'] = False
            int_point = int(point)
            point2 = -int_point
            pdate[user_id]['point'] = str(point2)
            seve2(user_id,point2)
            seve3(user_id)


    if '記録確認' == msg_text:
        line_bot_api.reply_message(msg_from,TextSendMessage(text='確認したい人の名前を教えてね！\n[打ち方]　確認:"名前"\n例: たろうくんの場合  確認:たろう'))


    if '確認:' in msg_text:
        name = msg_text.replace("確認:","")
        d = pointcheck(user_id,name)
        list2 = []
        for t in d:
            str_datetime = t[1].strftime('%Y-%m-%d %H:%M:%S')
            list2.append([t[0],str_datetime])
        list3 = []
        for t in list2:
            list3.append(' : '.join(t))
        date_str = '\n\n'.join(list3)
        line_bot_api.reply_message(msg_from,TextSendMessage(text='[今までの記録]\n{date_str}\n今の合計ポイント : {point}'.format(date_str=date_str,point=namecheck(user_id,name))))




if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
