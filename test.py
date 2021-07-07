import requests
import re
from lxml import etree
import time
from configparser import ConfigParser



if __name__=="__main__":
    config = ConfigParser()
    config.read('user.config')
    havingablums=[]
    count = config['ablums']['count']
    print("already have "+count+" ablums")
    for i in range(1,int(count)+1):
        a=config['ablums']['a'+str(i)]
        havingablums.append(a)
    for i in havingablums:
        print(i)
