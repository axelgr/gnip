# -*- coding: utf-8 -*-

import time
import datetime
from gnippy import PowerTrackClient
import json
from kafka import KafkaConsumer, KafkaProducer
from pyrichit3 import CognitiveRichit

#producer = KafkaProducer(bootstrap_servers='192.168.15.243:9092')
#servicebus = CognitiveRichit(urlfile = "/home/kafkaUser/gnip/entrenamiento_mx.csv")
#consumeGNIP = KafkaConsumer('tweet3',bootstrap_servers=['192.168.15.243:9092'])

def callback(activity):
    print("*")
     

client = PowerTrackClient(callback, config_file_path="/home/kafkaUser/gnip/gnippy.conf")
print("Init..")
client.connect()

time.sleep(10)

client.close()

print("off line")
