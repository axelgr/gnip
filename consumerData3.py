# -*- coding: utf-8 -*-

from pyrichit3 import CognitiveRichit
import re
from kafka import KafkaConsumer, KafkaProducer
import datetime
import json
import re
import os


servicebus = CognitiveRichit(urlfile = "/home/kafkaUser/gnip/entrenamiento_mx.csv")
tmpProducer = KafkaProducer(bootstrap_servers='localhost:9092')
consumeGNIP = KafkaConsumer('tweet3',bootstrap_servers=['localhost:9092'])

#tmpProducer.flush()
stopWords = ["\\n\\n","\\n","\\t","\\r"]


print("pykof3 ...")

def remove_emoji(data):
        if not data:
            return data
        if not isinstance(data, str):
            return data
        

        emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    
        return emoji_pattern.sub('', data)



def clearData(datax):        

    red = u'[^,\{\}\[\]\:\-\+\.\a-z\u00E7\u00F1\u00E1\u00E9\u00ED\u00F3\u00FA\u00E0\u00E8\u00EC\u00F2\u00F9\u00E4\u00EB\u00EF\u00F6\u00FC\u00E2\u00EA\u00EE\u00F4\u00FB]'
    
    if datax:
        for sw in stopWords:
            datax = datax.replace(sw,"")
    

    firstData = re.sub(red,'', re.sub('\n','',datax))
    return remove_emoji(firstData)


fileName = "{0}/{1}".format(os.getcwd(),"errors3.txt")
with open(fileName,'a') as f:   
    for mGnip in consumeGNIP:
    
        try:
        
            #st = servicebus.getSentiment(mGnip.value)
            st = mGnip.value

            dt = json.loads(st.decode("utf8", "replace"))
            sentiment = servicebus.getSentiment(st.decode("utf8", "replace"))
            dt["polarizacion"] = sentiment

            fecha = datetime.datetime.now()
            ider = str(fecha.strftime("%d%m%Y%H%M%S%f"))
            
            db = clearData(json.dumps(dt))

            f.write(db + "\n")

            print(".")
            #joinner = "\t".join([ider, json.dumps(dt)])
            #tmpIder = tmpProducer.send("tweets-json2", joinner)
            #f.write(json.dumps(dt) + "\n")

     
        except Exception as e:
            #f.writelines(mGnip.value)
            print(e)
