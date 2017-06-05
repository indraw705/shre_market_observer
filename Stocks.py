'''
Created on Feb 3, 2016

@author: indrajit.n
'''



from threading import Thread
from Tkinter import Label, Tk
import ctypes
import json
from pprint import pprint
import time
import urllib

from bs4 import BeautifulSoup
import easygui
from easygui.boxes.derived_boxes import msgbox
from pip._vendor.requests.packages.urllib3.util import url
import requests
import schedule
from twilio.rest import TwilioRestClient
import yaml

import xml.etree.ElementTree as ET


accountSid ="AC281d5a674d49e0b7ee9ad532f8c64ed0"
authToken ="34e100a04eb22ee343ef01c5d92c9a40"
lobbying = {}
hasSent=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

stockUrl=[]
stockName=[]
percentage=0.00
stockReferenceId=[]
MsgBox= ctypes.windll.user32.MessageBoxA   
#easygui.msgbox("This is a message!", title="simple gui")   this is also making window...

def fetchData():
    with open('Stocks.json') as data_file:    
        data=json.load(data_file)
        print hasSent
        print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        count=-1
        for item in data["stocks"]:
            count=count+1
            stockUrl="https://www.google.com/finance?q=NSE%3A"+item["url"]
            stockName=item["name"]
            stockReferenceId=item["refId"]
            stockReferencePer=item["refIdPer"]
            job(stockUrl, stockName, stockReferenceId,stockReferencePer,count,alert=0)
            
    data.get('url')

schedule.every(1).minutes.do(fetchData)

def job(stockUrl,stockName,stockReferenceId,stockReferencePer,count,alert):
        r=urllib.urlopen(stockUrl).read()    
        soup=BeautifulSoup(r , "html.parser")
        stockVal = soup.find_all("span", class_="pr")
        stockPercentage=soup.find_all("span",class_="ch bld")
        for element in stockPercentage:
            tempPercentage=element.find(id=stockReferencePer).get_text()
            percentage= tempPercentage.split("(")[1].split("%)")[0]
            
            print stockName+"\t"+percentage+"%"
            if abs(float(percentage)) <= (4.00):
                alert=1
            if abs(float(percentage))>=(8.50):
                sendSMS(stockName, percentage,count)
                hasSent[count]=1
        for element in stockVal:
            price = element.find(id=stockReferenceId).get_text()
            print  stockName+"\t"+price
            value=stockName+" "+str(price)+" INR \n and Stock is changed "+percentage+"%"
                
            if alert!=1:
                root = Tk()
                prompt = str(stockName)+'\n'+value
                label1 = Label(root, text=prompt, width=len(prompt))
                label1.pack()
                
                def close_after_2s():
                    root.destroy()
                    
                root.after(8000, close_after_2s)
                root.mainloop()
                 
def sendSMS(stockName,percentage,count):
    if hasSent[count]!=1:
        print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
        print "message is sending..."
        twilioClient = TwilioRestClient(accountSid, authToken)
        myTwilioNumber = "+12259537705"
        destCellPhone = "+919764846984"
        destCellPhone2 = "+919503740966"
        msgIs=stockName+ "  and it is changed with :"+percentage+"% !!!! this is system genarated msg  \n Do not reply"
        print "sending to indra"
        twilioClient.messages.create(body = "Hello, indra Stock "+msgIs, from_=myTwilioNumber, to=destCellPhone)
        print "sending to tanaji"
        twilioClient.messages.create(body = "Hello, Tanaji Stock "+msgIs, from_=myTwilioNumber, to=destCellPhone2)
    
# schedule.every().hour.do(job)
# schedule.every().day.at("09:30").do(job)
while 1:
    schedule.run_pending()
    time.sleep(1)

    

           
    
    