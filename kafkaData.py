reated on Thu Dec  1 18:04:56 2016

@author: axelgr
"""
from pyrichit import CognitiveRichit
from kafka import KafkaConsumer, KafkaProducer
import datetime
import json
import re



original = '{"id":"tag:search.twitter.com,2005:803354774569504768","objectType":"activity","verb":"post","postedTime":"2016-11-28T21:47:58.000Z","generator":{"displayName":"Instagram","link":"http:\/\/instagram.com"},"provider":{"objectType":"service","displayName":"Twitter","link":"http:\/\/www.twitter.com"},"link":"http:\/\/twitter.com\/mariag359\/statuses\/803354774569504768","body":"Tratando de mejorar poquito a poquito\ud83d\ude4f\ud83c\udffc\u26bd\ufe0f!! #estuvocerca #pasi\u00f3n @\u2026 https:\/\/t.co\/65Q7kxjClG","actor":{"objectType":"person","id":"id:twitter.com:260555642","link":"http:\/\/www.twitter.com\/mariag359","displayName":"Mariana","postedTime":"2011-03-04T03:12:49.000Z","image":"https:\/\/pbs.twimg.com\/profile_images\/801679379432620032\/X1XzejSG_normal.jpg","summary":null,"friendsCount":447,"followersCount":641,"listedCount":0,"statusesCount":20072,"twitterTimeZone":"Eastern Time (US & Canada)","verified":false,"utcOffset":"-18000","preferredUsername":"mariag359","languages":["es"],"links":[{"href":"http:\/\/m.ask.fm\/mariag359","rel":"me"}],"location":{"objectType":"place","displayName":"Campeche, M\u00e9xico"},"favoritesCount":4568},"object":{"objectType":"note","id":"object:search.twitter.com,2005:803354774569504768","summary":"Tratando de mejorar poquito a poquito\ud83d\ude4f\ud83c\udffc\u26bd\ufe0f!! #estuvocerca #pasi\u00f3n @\u2026 https:\/\/t.co\/65Q7kxjClG","link":"http:\/\/twitter.com\/mariag359\/statuses\/803354774569504768","postedTime":"2016-11-28T21:47:58.000Z"},"favoritesCount":0,"location":{"objectType":"place","displayName":"Campeche, M\u00e9xico","name":"Campeche","country_code":"M\u00e9xico","twitter_country_code":"MX","twitter_place_type":"city","link":"https:\/\/api.twitter.com\/1.1\/geo\/id\/6c726a9d72c3156e.json","geo":{"type":"Polygon","coordinates":[[[-90.693549,19.239300],[-90.693549,19.963528],[-89.860731,19.963528],[-89.860731,19.239300]]]}},"geo":{"type":"Point","coordinates":[19.87827484,-90.47610982]},"twitter_entities":{"hashtags":[{"text":"estuvocerca","indices":[44,56]},{"text":"pasi\u00f3n","indices":[57,64]}],"urls":[{"url":"https:\/\/t.co\/65Q7kxjClG","expanded_url":"https:\/\/www.instagram.com\/p\/BNXpUTDBagR2HOo-Y0iAlzDMYTbTcIPZX9qAAw0\/","display_url":"instagram.com\/p\/BNXpUTDBagR2\u2026","indices":[68,91]}],"user_mentions":[],"symbols":[]},"twitter_lang":"es","retweetCount":0,"gnip":{"matching_rules":[{"tag":"camp","id":802956608372293657}],"urls":[{"url":"https:\/\/t.co\/65Q7kxjClG","expanded_url":null,"expanded_status":null,"expanded_url_title":null,"expanded_url_description":null}]},"twitter_filter_level":"low"}'


servicebus = CognitiveRichit(urlfile = "/home/axelgr/Documents/RichIT/Drive/entrenamiento_mx.csv")
tmpProducer = KafkaProducer(bootstrap_servers='localhost:9092')
#original = '{"id":"elidsearc","objectType":"activity","verb":"share","postedTime":"2016-11-23T18:02:28.000Z","generator":{"displayName":"Twitter for iPhone","link":"http:\/\/twitter.com\/download\/iphone"},"provider":{"objectType":"service","displayName":"Twitter","link":"http:\/\/www.twitter.com"},"link":"http:\/\/twitter.com\/RichIbarraC\/statuses\/801486085498904576","body":"RT @JTrianaT: Di\u00e1logo en la C\u00e1mara de Diputados con los padres de los 43 normalistas de Ayotzinapa, exigen avance en las investigaciones\u2026","actor":{"objectType":"person","id":"id:twitter.com:441553181","link":"http:\/\/www.twitter.com\/RichIbarraC","displayName":"R I C H  I B A R R A","postedTime":"2011-12-20T06:05:57.000Z","image":"https:\/\/pbs.twimg.com\/profile_images\/795890166967791616\/DZ5WfeGh_normal.jpg","summary":"Oficio Pol\u00edtico. Servicio p\u00fablico. Derecho UNAM. Dem\u00f3crata, de centro y libertario. Aliancista. En la derecha del PRD, en la izquierda del PAN #AlianzaPANPRD","friendsCount":2291,"followersCount":1887,"listedCount":12,"statusesCount":10552,"twitterTimeZone":null,"verified":false,"utcOffset":null,"preferredUsername":"RichIbarraC","languages":["es"],"links":[{"href":null,"rel":"me"}],"location":{"objectType":"place","displayName":"Miguel Hidalgo, Distrito Federal"},"favoritesCount":13795},"object":{"id":"tag:search.twitter.com,2005:801485987071279104","objectType":"activity","verb":"post","postedTime":"2016-11-23T18:02:04.000Z","generator":{"displayName":"Twitter for iPhone","link":"http:\/\/twitter.com\/download\/iphone"},"provider":{"objectType":"service","displayName":"Twitter","link":"http:\/\/www.twitter.com"},"link":"http:\/\/twitter.com\/JTrianaT\/statuses\/801485987071279104","body":"Di\u00e1logo en la C\u00e1mara de Diputados con los padres de los 43 normalistas de Ayotzinapa, exigen avance en las investig\u2026 https:\/\/t.co\/SMQtlg4ddB","long_object":{"body":"Di\u00e1logo en la C\u00e1mara de Diputados con los padres de los 43 normalistas de Ayotzinapa, exigen avance en las investigaciones \n\n@diputadospan https:\/\/t.co\/ty0YkkMSxJ","display_text_range":[0,138],"twitter_entities":{"hashtags":[],"urls":[],"user_mentions":[{"screen_name":"diputadospan","name":"Diputados PAN","id":19545349,"id_str":"19545349","indices":[125,138]}],"symbols":[],"media":[{"id":801485872273104896,"id_str":"801485872273104896","indices":[139,162],"media_url":"http:\/\/pbs.twimg.com\/ext_tw_video_thumb\/801485872273104896\/pu\/img\/kPXsZhA-bVLMXcDR.jpg","media_url_https":"https:\/\/pbs.twimg.com\/ext_tw_video_thumb\/801485872273104896\/pu\/img\/kPXsZhA-bVLMXcDR.jpg","url":"https:\/\/t.co\/ty0YkkMSxJ","display_url":"pic.twitter.com\/ty0YkkMSxJ","expanded_url":"https:\/\/twitter.com\/JTrianaT\/status\/801485987071279104\/video\/1","type":"video","sizes":{"thumb":{"w":150,"h":150,"resize":"crop"},"medium":{"w":600,"h":338,"resize":"fit"},"small":{"w":340,"h":191,"resize":"fit"},"large":{"w":1024,"h":576,"resize":"fit"}},"video_info":{"aspect_ratio":[16,9],"duration_millis":53433,"variants":[{"bitrate":832000,"content_type":"video\/mp4","url":"https:\/\/video.twimg.com\/ext_tw_video\/801485872273104896\/pu\/vid\/640x360\/3F_LEUx_nh0ki3jZ.mp4"},{"bitrate":2176000,"content_type":"video\/mp4","url":"https:\/\/video.twimg.com\/ext_tw_video\/801485872273104896\/pu\/vid\/1280x720\/o_n9cL2fQ8vE-Vcm.mp4"},{"bitrate":320000,"content_type":"video\/mp4","url":"https:\/\/video.twimg.com\/ext_tw_video\/801485872273104896\/pu\/vid\/320x180\/vSwBR1zEtFE2Hp4H.mp4"},{"content_type":"application\/x-mpegURL","url":"https:\/\/video.twimg.com\/ext_tw_video\/801485872273104896\/pu\/pl\/RE9pRlw-TmgUIBpD.m3u8"},{"content_type":"application\/dash+xml","url":"https:\/\/video.twimg.com\/ext_tw_video\/801485872273104896\/pu\/pl\/RE9pRlw-TmgUIBpD.mpd"}]}}]},"twitter_extended_entities":{"media":[{"id":801485872273104896,"id_str":"801485872273104896","indices":[139,162],"media_url":"http:\/\/pbs.twimg.com\/ext_tw_video_thumb\/801485872273104896\/pu\/img\/kPXsZhA-bVLMXcDR.jpg","media_url_https":"https:\/\/pbs.twimg.com\/ext_tw_video_thumb\/801485872273104896\/pu\/img\/kPXsZhA-bVLMXcDR.jpg","url":"https:\/\/t.co\/ty0YkkMSxJ","display_url":"pic.twitter.com\/ty0YkkMSxJ","expanded_url":"https:\/\/twitter.com\/JTrianaT\/status\/801485987071279104\/video\/1","type":"video","sizes":{"thumb":{"w":150,"h":150,"resize":"crop"},"medium":{"w":600,"h":338,"resize":"fit"},"small":{"w":340,"h":191,"resize":"fit"},"large":{"w":1024,"h":576,"resize":"fit"}},"video_info":{"aspect_ratio":[16,9],"duration_millis":53433,"variants":[{"bitrate":832000,"content_type":"video\/mp4","url":"https:\/\/video.twimg.com\/ext_tw_video\/801485872273104896\/pu\/vid\/640x360\/3F_LEUx_nh0ki3jZ.mp4"},{"bitrate":2176000,"content_type":"video\/mp4","url":"https:\/\/video.twimg.com\/ext_tw_video\/801485872273104896\/pu\/vid\/1280x720\/o_n9cL2fQ8vE-Vcm.mp4"},{"bitrate":320000,"content_type":"video\/mp4","url":"https:\/\/video.twimg.com\/ext_tw_video\/801485872273104896\/pu\/vid\/320x180\/vSwBR1zEtFE2Hp4H.mp4"},{"content_type":"application\/x-mpegURL","url":"https:\/\/video.twimg.com\/ext_tw_video\/801485872273104896\/pu\/pl\/RE9pRlw-TmgUIBpD.m3u8"},{"content_type":"application\/dash+xml","url":"https:\/\/video.twimg.com\/ext_tw_video\/801485872273104896\/pu\/pl\/RE9pRlw-TmgUIBpD.mpd"}]}}]}},"display_text_range":[0,140],"actor":{"objectType":"person","id":"id:twitter.com:42558679","link":"http:\/\/www.twitter.com\/JTrianaT","displayName":"Jorge Triana","postedTime":"2009-05-26T03:52:31.000Z","image":"https:\/\/pbs.twimg.com\/profile_images\/797699549103988736\/R-JFtA0C_normal.jpg","summary":"Diputado Federal || Tanta sociedad como sea posible, y s\u00f3lo tanto gobierno como sea necesario. #DiputadoADomicilio #MiguelHidalgo","friendsCount":613,"followersCount":18117,"listedCount":111,"statusesCount":25662,"twitterTimeZone":"Mexico City","verified":false,"utcOffset":"-21600","preferredUsername":"JTrianaT","languages":["es"],"links":[{"href":"http:\/\/www.jorgetriana.com.mx","rel":"me"}],"location":{"objectType":"place","displayName":"Miguel Hidalgo, CDMX"},"favoritesCount":2885},"object":{"objectType":"note","id":"object:search.twitter.com,2005:801485987071279104","summary":"Di\u00e1logo en la C\u00e1mara de Diputados con los padres de los 43 normalistas de Ayotzinapa, exigen avance en las investig\u2026 https:\/\/t.co\/SMQtlg4ddB","link":"http:\/\/twitter.com\/JTrianaT\/statuses\/801485987071279104","postedTime":"2016-11-23T18:02:04.000Z"},"favoritesCount":0,"twitter_entities":{"hashtags":[],"urls":[{"url":"https:\/\/t.co\/SMQtlg4ddB","expanded_url":"https:\/\/twitter.com\/i\/web\/status\/801485987071279104","display_url":"twitter.com\/i\/web\/status\/8\u2026","indices":[117,140]}],"user_mentions":[],"symbols":[]},"twitter_lang":"es","twitter_filter_level":"low"},"favoritesCount":0,"twitter_entities":{"hashtags":[],"urls":[],"user_mentions":[{"screen_name":"JTrianaT","name":"Jorge Triana","id":42558679,"id_str":"42558679","indices":[3,12]}],"symbols":[]},"twitter_lang":"es","retweetCount":1,"gnip":{"matching_rules":[{"tag":null,"id":798291286776123392}]},"twitter_filter_level":"low"}'

#servicebus.regenerateData(original)


tmpIder = tmpProducer.send("gnipTopic",  servicebus.regenerateData(original))

record_metadata = tmpIder.get(timeout=10)
record_metadata.offset

#****************************Consume GNIP *************************

KafkaConsumer(consumer_timeout_ms=1000)
consumeGNIP = KafkaConsumer('gnipTopic',bootstrap_servers=['localhost:9092'])
#consumeGNIP(value_deserializer=lambda m: json.loads(m.decode('ascii')))
for mGnip in consumeGNIP:
    print mGnip.value


    