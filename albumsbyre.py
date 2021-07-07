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
        qyid = 'wwbce37d7e2b926c5d'
        miyue = 'sxCU_Bjk92_171_V4sGvAFRC4NPeVCAlwoI0nYrpBgY'
        appid = '1000002'
        # card massage
        url2 = 'https://api.htm.fun/api/Wechat/text_card/'
        title = '点击领取新的数字专辑啦！'
        description = 'descriptionaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        url = 'https://chen310.github.io/music/albums/'
        r2 = requests.get(url2, params={"corpid": qyid, "corpsecret": miyue, "agentid": appid, "title": title,
                                        "description": description, "url": url})
        ReConfig("setting","timestamp",str(timestamp))
        return 1
    else:
        return 0

#get config
def GetConfig():
    config=ConfigParser()
    config.read('user.config', encoding='UTF-8-sig')
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
    config.read('user.config', encoding='UTF-8-sig')
    config.set(section,name,v)
    config.write(open('user.config', "w"))
    print("re-configed")

#have update
def Updata(html):
    pass
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
    #print(r.content.decode("utf-8"))
    #html = etree.HTML(r.content.decode("utf-8"))
    #recently=html.xpath('//*[@id="post-领取网易云音乐数字专辑"]/div[2]/p[1]/text()')
    recently=re.findall(r'>数据更新于*<',r.content.decode("utf-8"))
    print(recently)
    recently=recently[0].split('于')[1]
    #time to timestamp
    timestamp=int(time.mktime(time.strptime(recently, '%Y-%m-%d %H:%M:%S')))
    print("recently update-time:"+recently+";timestamp is "+str(timestamp))
    if(IfUpdate(config['initstamp'],timestamp)):
        Updata(html)
    else:
        print("havn't updated")