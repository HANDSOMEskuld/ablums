import requests
import re
#from lxml import etree
import time
from configparser import ConfigParser

#find update time
def IfUpdate(initstamp,timestamp):
    #initstamp=int(1625553629)
    if (timestamp>initstamp):
        print("have updated")
        ReConfig("setting","timestamp",str(timestamp))
        return 1
    else:
        return 0

#missage
def Push(ablums,count,time):
    if count==0:
        print("cancel pushing")
        return
    qyid = 'wwbce37d7e2b926c5d'
    miyue = 'sxCU_Bjk92_171_V4sGvAFRC4NPeVCAlwoI0nYrpBgY'
    appid = '1000002'
    # card massage
    url2 = 'https://api.htm.fun/api/Wechat/text_card/'
    title = '点击领取新的'+str(count)+'张数字专辑啦！'
    des=''
    for i in ablums:
        des=des+'·'+i+'\n'
    description='更新时间：'+time+'\n'+des+'斯人若彩虹，遇上方知有'
    #description = '<div class=\"gray\">'+time+'</div> <div class=\"normal\"> '+des+'</div>共有'+str(count)+'张专辑<div class=\"highlight\">斯人若彩虹，遇上方知有</div>"'
    print(description)
    url = 'https://chen310.github.io/music/albums/'
    r2 = requests.get(url2, params={"corpid": qyid, "corpsecret": miyue, "agentid": appid, "title": title,
                                    "description": description, "url": url})
    print("have pushed")

#get config
def GetConfig():
    config=ConfigParser()
    config.read('user.config', encoding='GBK')
    initstamp=config['setting']['timestamp']
    url=config['setting']['url']
    vipday=config['vip']['day']
    conf = {
        'initstamp': int(initstamp),
        'url': url,
        'vipday': vipday
    }
    return conf

#change config
def ReConfig(section,name,v):
    config = ConfigParser()
    config.read('user.config', encoding='GBK')
    config.set(section,name,v)
    config.write(open('user.config', "w"))
    print("re-configed")

#get having ablumes
def GetHave():
    config = ConfigParser()
    config.read('user.config', encoding='GBK')
    havingablums = []
    count = config['ablums']['count']
    print("already have " + count + " ablums")
    for i in range(1, int(count) + 1):
        a = config['ablums']['a' + str(i)]
        havingablums.append(a)
    return havingablums

#have update
def Updata(time,r):
    r=r.replace(' ','')
    num=0
    count=0
    ablums=[]
    a = re.findall(r'([pr])>(.*?)\(', r)
    havingablums=GetHave()
    for i in a:
        if i[0]=='p':
            num=num+1
            if num==2:
                break
        #have or not
        if i[1] in havingablums:
            continue
        else:
            count=count+1
            ablums.append(i[1])
        print(i[1])
    print("new albums:",count)
    Push(ablums,count,time)
    #ablums=html.xpath


if __name__=="__main__":
    print("start processing")
    config=GetConfig()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}
    #print(config['url'])
    r=requests.get(config['url'], headers=headers)
    #time.sleep(3)
    if(r.status_code==200):
        print("connecting finished")
    else:
        print("connecting error,please retry")
    #find update time
    r=r.content.decode("utf-8")
    recently=re.findall(r'\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}',r)
    #print(r)
    recently=recently[0]
    #time to timestamp
    timestamp=int(time.mktime(time.strptime(recently, '%Y-%m-%d %H:%M:%S')))
    print("recently update-time:"+recently+";timestamp is "+str(timestamp))
    if(IfUpdate(config['initstamp'],timestamp)):
        Updata(recently,r)
    else:
        print("havn't updated")
