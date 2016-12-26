from pyrichit import CognitiveRichit
from kafka import KafkaConsumer, KafkaProducer
import datetime
import json
import re


original = '{"id":"tag:search.twitter.com,2005:803354774569504768","objectType":"activity","verb":"post","postedTime":"2016-11-28T21:47:58.000Z","generator":{"displayName":"Instagram","link":"http:\/\/instagram.com"},"provider":{"objectType":"service","displayName":"Twitter","link":"http:\/\/www.twitter.com"},"link":"http:\/\/twitter.com\/mariag359\/statuses\/803354774569504768","body":"Tratando de mejorar poquito a poquito\ud83d\ude4f\ud83c\udffc\u26bd\ufe0f!! #estuvocerca #pasi\u00f3n @\u2026 https:\/\/t.co\/65Q7kxjClG","actor":{"objectType":"person","id":"id:twitter.com:260555642","link":"http:\/\/www.twitter.com\/mariag359","displayName":"Mariana","postedTime":"2011-03-04T03:12:49.000Z","image":"https:\/\/pbs.twimg.com\/profile_images\/801679379432620032\/X1XzejSG_normal.jpg","summary":null,"friendsCount":447,"followersCount":641,"listedCount":0,"statusesCount":20072,"twitterTimeZone":"Eastern Time (US & Canada)","verified":false,"utcOffset":"-18000","preferredUsername":"mariag359","languages":["es"],"links":[{"href":"http:\/\/m.ask.fm\/mariag359","rel":"me"}],"location":{"objectType":"place","displayName":"Campeche, M\u00e9xico"},"favoritesCount":4568},"object":{"objectType":"note","id":"object:search.twitter.com,2005:803354774569504768","summary":"Tratando de mejorar poquito a poquito\ud83d\ude4f\ud83c\udffc\u26bd\ufe0f!! #estuvocerca #pasi\u00f3n @\u2026 https:\/\/t.co\/65Q7kxjClG","link":"http:\/\/twitter.com\/mariag359\/statuses\/803354774569504768","postedTime":"2016-11-28T21:47:58.000Z"},"favoritesCount":0,"location":{"objectType":"place","displayName":"Campeche, M\u00e9xico","name":"Campeche","country_code":"M\u00e9xico","twitter_country_code":"MX","twitter_place_type":"city","link":"https:\/\/api.twitter.com\/1.1\/geo\/id\/6c726a9d72c3156e.json","geo":{"type":"Polygon","coordinates":[[[-90.693549,19.239300],[-90.693549,19.963528],[-89.860731,19.963528],[-89.860731,19.239300]]]}},"geo":{"type":"Point","coordinates":[19.87827484,-90.47610982]},"twitter_entities":{"hashtags":[{"text":"estuvocerca","indices":[44,56]},{"text":"pasi\u00f3n","indices":[57,64]}],"urls":[{"url":"https:\/\/t.co\/65Q7kxjClG","expanded_url":"https:\/\/www.instagram.com\/p\/BNXpUTDBagR2HOo-Y0iAlzDMYTbTcIPZX9qAAw0\/","display_url":"instagram.com\/p\/BNXpUTDBagR2\u2026","indices":[68,91]}],"user_mentions":[],"symbols":[]},"twitter_lang":"es","retweetCount":0,"gnip":{"matching_rules":[{"tag":"camp","id":802956608372293657}],"urls":[{"url":"https:\/\/t.co\/65Q7kxjClG","expanded_url":null,"expanded_status":null,"expanded_url_title":null,"expanded_url_description":null}]},"twitter_filter_level":"low"}'
servicebus = CognitiveRichit(urlfile = "/home/axelgr/Documents/RichIT/Drive/entrenamiento_mx.csv")
tmpProducer = KafkaProducer(bootstrap_servers='localhost:9092')
tmpIder = tmpProducer.send("gnipTopic",  servicebus.regenerateData(original))

record_metadata = tmpIder.get(timeout=10)
record_metadata.offset

#****************************Consume GNIP *************************

KafkaConsumer(consumer_timeout_ms=1000)
consumeGNIP = KafkaConsumer('gnipTopic',bootstrap_servers=['localhost:9092'])
#consumeGNIP(value_deserializer=lambda m: json.loads(m.decode('ascii')))
for mGnip in consumeGNIP:
    print mGnip.value
