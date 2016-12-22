# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 11:30:09 2016

@author: axelgr
"""


import json
import pprint

import re
import datetime
import pandas as pd
from pyrichit import CognitiveRichit 
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import RidgeClassifier
from sklearn.multiclass import OneVsRestClassifier

headersFace = None
headersText = None
paramsFace = None
paramsText = None

stopWords= ["\n\n","\n","\t", "\r"]

headersFace = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '87d177469c704d84b9705cc82f4502c2'
}

paramsFace = urllib.urlencode({
    # Request parameters
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,smile',
})

headersText = {
        # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '889700046451456cbfa8c4affe53b9f7'
}

paramsText = urllib.urlencode({
})




def callCognitiveFaceApi( mediaUrl):
        
    if mediaUrl:
        jbody = "{'url': '%s'}" % mediaUrl
   
   
        try:
            
            conn = httplib.HTTPSConnection('api.projectoxford.ai')
            conn.request("POST", "/face/v1.0/detect?%s" % params, jbody, headers)
            response = conn.getresponse()
            data = response.read()
            
            
            pprint.pprint(data)
            
            print "--------------"
            faceData = json.loads(data)    
            
            if not len(faceData):
                for f in faceData:
                    pprint.pprint(f)
            
          #  pprint.pprint(faceData)
    
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
   
   
   
def callCognitiveSentimentApi(texter):
    jsSentimentText = None


    if texter:    
    
        try:
            conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
            conn.request("POST", "/text/analytics/v2.0/sentiment?%s" % paramsText, texter, headersText)
            response = conn.getresponse()
            jsSentimentText = response.read()
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    return jsSentimentText



#if 'twitter_extended_entities' in jsData.keys():
#    mediaCount = len(jsData['twitter_extended_entities']['media'])
   
    
    #if mediaCount == 1:
    #   jPhoto = str(jsData['twitter_extended_entities']['media'][0]['media_url_https'])
    #   print jPhoto
    #elif mediaCount >1:
     
#    for tw in jsData['twitter_extended_entities']['media']:
#        print tw['media_url_https']
       #callCognitiveFaceApi(str(m['media_url']))   

####################################


#without tweet
#original_tweet = '{"id":"tag:search.twitter.com,2005:801573249226186752","objectType":"activity","verb":"post","postedTime":"2016-11-23T23:48:49.000Z","generator":{"displayName":"Twitter Web Client","link":"http:\/\/twitter.com"},"provider":{"objectType":"service","displayName":"Twitter","link":"http:\/\/www.twitter.com"},"link":"http:\/\/twitter.com\/Tlahuicole1318\/statuses\/801573249226186752","body":"@Lilicio5973 desgracia chaira el efecto @lopezobrador_ solo terminara beneficiando a una PEOR es decir a @Mzavalagc #NadieSabePaQuienTrabaja","display_text_range":[13,140],"actor":{"objectType":"person","id":"id:twitter.com:1884260971","link":"http:\/\/www.twitter.com\/Tlahuicole1318","displayName":"El Torito Mexicano","postedTime":"2013-09-19T20:01:43.751Z","image":"https:\/\/pbs.twimg.com\/profile_images\/672556166430371840\/eCkQyGlh_normal.jpg","summary":"el Maltrato animal es el  fracaso de la inteligencia Humana.","friendsCount":8595,"followersCount":8742,"listedCount":47,"statusesCount":68038,"twitterTimeZone":"Mexico City","verified":false,"utcOffset":"-21600","preferredUsername":"Tlahuicole1318","languages":["es"],"links":[{"href":null,"rel":"me"}],"favoritesCount":615},"object":{"objectType":"note","id":"object:search.twitter.com,2005:801573249226186752","summary":"@Lilicio5973 desgracia chaira el efecto @lopezobrador_ solo terminara beneficiando a una PEOR es decir a @Mzavalagc #NadieSabePaQuienTrabaja","link":"http:\/\/twitter.com\/Tlahuicole1318\/statuses\/801573249226186752","postedTime":"2016-11-23T23:48:49.000Z"},"inReplyTo":{"link":"http:\/\/twitter.com\/Lilicio5973\/statuses\/801571893178417152"},"favoritesCount":0,"twitter_entities":{"hashtags":[{"text":"NadieSabePaQuienTrabaja","indices":[116,140]}],"urls":[],"user_mentions":[{"screen_name":"Lilicio5973","name":"lilia del rocio mont","id":294415308,"id_str":"294415308","indices":[0,12]},{"screen_name":"lopezobrador_","name":"Andr\u00e9s Manuel","id":82119937,"id_str":"82119937","indices":[40,54]},{"screen_name":"Mzavalagc","name":"Margarita Zavala","id":97017966,"id_str":"97017966","indices":[105,115]}],"symbols":[]},"twitter_lang":"es","retweetCount":0,"gnip":{"matching_rules":[{"tag":null,"id":798291286776123392}]},"twitter_filter_level":"low"}'

def getSentiment(original_tweet):
    jsTweet = json.loads(original_tweet)
    retweet = 0
    jsBody = None
    
    if 'retweetCount' in jsTweet.keys():
        retweet = jsTweet.get('retweetCount')
        
        if retweet > 0 and 'twitter_quoted_status' in jsTweet.keys():
            jsBody = jsTweet.get('twitter_quoted_status').get('body')

        else:
            jsBody = jsTweet.get('body')
    
    
    
    if jsBody:    
        jsBodyReplace = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', jsBody, flags=re.MULTILINE)
        jsBody = jsBodyReplace
    
    dateDoc = datetime.datetime.now()
    jsId = dateDoc.strftime("%d%m%Y%H%M%S%f")
    
    
    jsAnalysis = callCognitiveSentimentApi('{"documents": [{"id": '+ jsId +',"language":"es","text": "'+ jsBody.encode("utf8") + '"}]}')
    score = 0
    
    if jsAnalysis:
        jsResponse = json.loads(jsAnalysis)
        
        if len(jsResponse.get("documents")) > 0:
            score = jsResponse.get("documents")[0].get("score")
            
    return score
    
def cognitiveText(metadata):
        pred_test = None
        csvData = None
        csvData = pd.read_csv("/home/axelgr/Documents/RichIT/Drive/entrenamiento_mx.csv")
        csvData = csvData[[0,1]]   
    
        X_train = csvData['texto']
        y_train = csvData['polaridad']
        
        classifier_Ridge = Pipeline([
            ('vectorizer', CountVectorizer()),
            ('tfidf', TfidfTransformer()),
            ('clf', OneVsRestClassifier(RidgeClassifier()))])
    
        classifier_Ridge.fit(X_train, y_train)
        pred_test = classifier_Ridge.predict(metadata)
        
        
        return pred_test
        
        
        
####################################

stopWords = ["\\n\\n","\\n","\\t","\\r"]




def remove_emoji(data):
	if not data:
            return data
	if not isinstance(data, basestring):
            return data
	try:
	# UCS-4
    	    patt = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
	except re.error:
	# UCS-2
    	    patt = re.compile(u'([\ufe00-\ufeff])|([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')
        return patt.sub('', data)






def clearData(datax):        

        red = ur'[^,\{\}\[\]\:\-\+\.\a-z\u00E7\u00F1\u00E1\u00E9\u00ED\u00F3\u00FA\u00E0\u00E8\u00EC\u00F2\u00F9\u00E4\u00EB\u00EF\u00F6\u00FC\u00E2\u00EA\u00EE\u00F4\u00FB ]'
    
        if datax:
            for sw in stopWords:
                datax = datax.replace(sw,"")
    
        
        #return re.sub(red,'', re.sub('\n','',datax))
        firstData = re.sub(red,'', re.sub('\n','',datax))
    	return remove_emoji(firstData)


def clearity(dirtytxt):
    texting = dirtytxt
    
    if texting:
        charser = {'\\u00c1' : 'Á','\\u00e1':'á','\\u00c9':'É', '\\u00e9':'é','\\u00cd':'Í','\\u00ED':'í','\\u00d3':'Ó','\\u00f3':'ó','\\u00da':'Ú','\\u00fa':'ú','\\u00d1':'Ñ','\\u00f1':'ñ', '\\u00dc':'Ü', '\\u00fc':'ü','\\u0022':'"','\\u0027':'\''}
        for c in charser:texting = texting.replace(c,charser[c])
        patt = re.compile(u'(\\\\u+\w{4})', re.MULTILINE | re.IGNORECASE | re.DOTALL)
    	texting = patt.sub('', texting)
    

    return texting


def getSentiment(datax):
    gJson = None
    richJson = None
    retweet = 0
    jsBody = None
    gBody = []
    jSentiment  = None
    richSent = "NEUTRAL"
         

    if datax:
                    
        try:
                                
            richJson = json.loads(datax)    
                
                
            if 'retweetCount' in richJson.keys():
                jretweet = richJson.get('retweetCount')
                    
                if jretweet > 0 and 'twitter_quoted_status' in richJson.keys():
                    jsBody = richJson.get('twitter_quoted_status').get('body')
            
                else:
                    jsBody = richJson.get('body')
                                
                
            if jsBody:
                    
                jsBody = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', jsBody, flags=re.MULTILINE)
                jsBody = clearData(jsBody)

            gBody.append(jsBody) 
            #print gBody                 
            jSentiment = cognitiveText(gBody)
                         
                    
                
            if jSentiment:
                richSent = jSentiment
    
        except Exception as e:
            richSent = "NEUTRAL"
            print e
                #print "*******************************************"
	        #print datax

    #self.getSentiment(richJson)	
            

        #jSentiment = richSent
        
	#print richSent
    return richSent

try:
    from pyrichit import CognitiveRichit 
    #original = "{\"id\":\"tag:search.twitter.com,2005:805846567160836096\",\"objectType\":\"activity\",\"verb\":\"post\",\"postedTime\":\"2016-12-05T18:49:28.000Z\",\"generator\":{\"displayName\":\"Twitter for iPhone\",\"link\":\"http:\\/\\/twitter.com\\/download\\/iphone\"},\"provider\":{\"objectType\":\"service\",\"displayName\":\"Twitter\",\"link\":\"http:\\/\\/www.twitter.com\"},\"link\":\"http:\\/\\/twitter.com\\/MauricioCuevass\\/statuses\\/805846567160836096\",\"body\":\"Decid\\u00ed alejarme \\u03b1\\ud83d\\udc95Coderera una tortura para m\\u00ed solo pensar que pod\\u00eda sufrir m\\u00e1s viviendo ilusionado que alg\\u00fan d\\u00eda ella ser\\u00eda para m\\u00ed.\",\"actor\":{\"objectType\":\"person\",\"id\":\"id:twitter.com:190299899\",\"link\":\"http:\\/\\/www.twitter.com\\/MauricioCuevass\",\"displayName\":\"Mauricio Cuevass\",\"postedTime\":\"2010-09-13T16:12:22.000Z\",\"image\":\"https:\\/\\/pbs.twimg.com\\/profile_images\\/800579029573271552\\/BvEyqO7d_normal.jpg\",\"summary\":\"\\/Temeroso de Dios\\/No me sigas no se a donde voy\\/Cantante de m\\u00fasica urbana\\/Luchemos por nuestros sue\\u00f1os\\/Influencer \\/Pumista\\/Chiapas\\/\",\"friendsCount\":255,\"followersCount\":477,\"listedCount\":6,\"statusesCount\":28227,\"twitterTimeZone\":\"Central Time (US & Canada)\",\"verified\":false,\"utcOffset\":\"-21600\",\"preferredUsername\":\"MauricioCuevass\",\"languages\":[\"es\"],\"links\":[{\"href\":\"https:\\/\\/www.youtube.com\\/user\\/EZLNBOLG\\/videos\",\"rel\":\"me\"}],\"location\":{\"objectType\":\"place\",\"displayName\":\"Tuxtla Gutierrez, Chiapas\"},\"favoritesCount\":796},\"object\":{\"objectType\":\"note\",\"id\":\"object:search.twitter.com,2005:805846567160836096\",\"summary\":\"Decid\\u00ed alejarme era una tortura para m\\u00ed solo pensar que pod\\u00eda sufrir m\\u00e1s viviendo ilusionado que alg\\u00fan d\\u00eda ella ser\\u00eda para m\\u00ed.\",\"link\":\"http:\\/\\/twitter.com\\/MauricioCuevass\\/statuses\\/805846567160836096\",\"postedTime\":\"2016-12-05T18:49:28.000Z\"},\"favoritesCount\":0,\"location\":{\"objectType\":\"place\",\"displayName\":\"Tuxtla Guti\\u00e9rrez, Chiapas\",\"name\":\"Tuxtla Guti\\u00e9rrez\",\"country_code\":\"M\\u00e9xico\",\"twitter_country_code\":\"MX\",\"twitter_place_type\":\"city\",\"link\":\"https:\\/\\/api.twitter.com\\/1.1\\/geo\\/id\\/b462c87ea2b4ff26.json\",\"geo\":{\"type\":\"Polygon\",\"coordinates\":[[[-93.243094,16.645909],[-93.243094,16.838962],[-93.036225,16.838962],[-93.036225,16.645909]]]}},\"twitter_entities\":{\"hashtags\":[],\"urls\":[],\"user_mentions\":[],\"symbols\":[]},\"twitter_lang\":\"es\",\"retweetCount\":0,\"gnip\":{\"matching_rules\":[{\"tag\":\"chis\",\"id\":804410079092949006}]},\"twitter_filter_level\":\"low\"}"

    original = "{\"id\":\"tag:search.twitter.com,2005:809896168046133249\",\"objectType\":\"activity\",\"verb\":\"post\",\"postedTime\":\"2016-12-16T23:01:08.000Z\",\"generator\":{\"displayName\":\"Twitter Web Client\",\"link\":\"http:\\/\\/twitter.com\"},\"provider\":{\"objectType\":\"service\",\"displayName\":\"Twitter\",\"link\":\"http:\\/\\/www.twitter.com\"},\"link\":\"http:\\/\\/twitter.com\\/TuzMay\\/statuses\\/809896168046133249\",\"body\":\"ya casi 2017 y la solter\\u00eda sigue jejjejee :3 #Vestir\\u00e9Santos jajjaja #xD\",\"actor\":{\"objectType\":\"person\",\"id\":\"id:twitter.com:295828969\",\"link\":\"http:\\/\\/www.twitter.com\\/TuzMay\",\"displayName\":\"Rodrigo tuz may\",\"postedTime\":\"2011-05-09T18:44:40.000Z\",\"image\":\"https:\\/\\/pbs.twimg.com\\/profile_images\\/624798016273145856\\/vRm4OgMV_normal.jpg\",\"summary\":\"Estudiante de la Universidad Intercultural Maya de Quintana Roo en Ing. Tecnolog\\u00edas de la informaci\\u00f3n y comunicaci\\u00f3n\",\"friendsCount\":84,\"followersCount\":78,\"listedCount\":5,\"statusesCount\":2551,\"twitterTimeZone\":null,\"verified\":false,\"utcOffset\":null,\"preferredUsername\":\"TuzMay\",\"languages\":[\"es\"],\"links\":[{\"href\":\"http:\\/\\/www.facebook.com\\/rodrigo.tuzmay\",\"rel\":\"me\"}],\"location\":{\"objectType\":\"place\",\"displayName\":\"Jose Mar\\u00eda Morelos, Q.roo. mx\"},\"favoritesCount\":323},\"object\":{\"objectType\":\"note\",\"id\":\"object:search.twitter.com,2005:809896168046133249\",\"summary\":\"ya casi 2017 y la solter\\u00eda sigue jejjejee :3 #Vestir\\u00e9Santos jajjaja #xD\",\"link\":\"http:\\/\\/twitter.com\\/TuzMay\\/statuses\\/809896168046133249\",\"postedTime\":\"2016-12-16T23:01:08.000Z\"},\"favoritesCount\":0,\"location\":{\"objectType\":\"place\",\"displayName\":\"Benito Ju\\u00e1rez, Distrito Federal\",\"name\":\"Benito Ju\\u00e1rez\",\"country_code\":\"M\\u00e9xico\",\"twitter_country_code\":\"MX\",\"twitter_place_type\":\"city\",\"link\":\"https:\\/\\/api.twitter.com\\/1.1\\/geo\\/id\\/7d93122509633720.json\",\"geo\":{\"type\":\"Polygon\",\"coordinates\":[[[-99.191996,19.357102],[-99.191996,19.404124],[-99.130965,19.404124],[-99.130965,19.357102]]]}},\"twitter_entities\":{\"hashtags\":[{\"text\":\"Vestir\\u00e9Santos\",\"indices\":[45,59]},{\"text\":\"xD\",\"indices\":[68,71]}],\"urls\":[],\"user_mentions\":[],\"symbols\":[]},\"twitter_lang\":\"es\",\"retweetCount\":0,\"gnip\":{\"matching_rules\":[{\"tag\":\"edo_mex\",\"id\":804410079092949009},{\"tag\":\"cdmx\",\"id\":804410079092949020}]},\"twitter_filter_level\":\"low\"}"
    
    #"J\\u03b9m\\u03b5\\u03b7\\u03b1\\ud83d\\udc95Coder\\ud83d\\udc95Due\\u00f1a de : @cd9_queretaro\\u2022A l o n s o\\u2022"
    
    #clean = patt.sub('', codr.decode("unicode-escape"))
        
    #liner = json.loads(unicode(data, errors='ignore'))
    
    dt = remove_emoji(original)
    
    clnJson = clearData(dt)
    
   
    servicebus = CognitiveRichit(urlfile = '')
    #st = servicebus.regenerateData(clnJson) 
    st = servicebus.getSentiment(clnJson)
                
    fecha = datetime.datetime.now()
    ider = str(fecha.strftime("%d%m%Y%H%M%S%f"))
    
   
    clnJson = clearity(clnJson)    

    clnJson = unicode(clnJson, "utf-8")
    json.dumps(clnJson)
    joinner = "\t".join([ider, json.dumps(st)])
    joinner = joinner + "\n"
    #type(clnJson)    
    
    
   #func    
    #jsTweet = json.loads(clnJson)
    #thesentiment = getSentiment(clnJson)
    #print thesentiment
    #jsTweet["polarizacion"] = str(thesentiment)

    try:
    # UCS-4
        highpoints = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
    # UCS-2
        highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
# mytext = u'<some string containing 4-byte chars>'
    mytext = highpoints.sub(u'', original)
    
    #end
    fecha = datetime.datetime.now()
    ider = str(fecha.strftime("%d%m%Y%H%M%S%f"))
    joinner = "\t".join([ider, json.dumps(st)])
    joinner = joinner + "\n"
    
    
    j = open('/home/axelgr/Documents/RichIT/Gnip/xample.json', 'r+')
    j.writelines(joinner)    
    j.close()
    #tmpIder = tmpProducer.send("tweets-json2", joinner)
    print "~"
        

except Exception as e:
    #print clnJson
    #print e
    print e
        #theinput = raw_input()
        
        

