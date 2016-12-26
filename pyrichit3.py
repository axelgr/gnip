
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 13:43:21 2016

@author: axelgr
"""
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import RidgeClassifier
from sklearn.multiclass import OneVsRestClassifier

import datetime
import json
import re

class CognitiveRichit:
    
    urlfile = None
    stopWords = ["\\n\\n","\\n","\\t","\\r"]
    csvData = None
    jSentiment = None


    def __init__(self, urlfile):        
        self.urlfile = urlfile
        self.csvData = pd.read_csv(urlfile)        
        
        
    def clearData(self, datax):        
        red = u'[^,\{\}\[\]\:\-\+\.\a-z\u00E7\u00F1\u00E1\u00E9\u00ED\u00F3\u00FA\u00E0\u00E8\u00EC\u00F2\u00F9\u00E4\u00EB\u00EF\u00F6\u00FC\u00E2\u00EA\u00EE\u00F4\u00FB]'
    
        if datax:
            for sw in self.stopWords:
                datax = datax.replace(sw,"")
    
        #firstClean = 

        return re.sub(red,'', re.sub('\n','',datax))

        #return remove_emoji(firstData)

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


    def clearity(dirtytxt):
        texting = dirtytxt
	
        if texting:
            charser = {'\\u00c1' : 'Á','\\u00e1':'á','\\u00c9':'É', '\\u00e9':'é','\\u00cd':'Í','\\u00ED':'í','\\u00d3':'Ó','\\u00f3':'ó','\\u00da':'Ú','\\u00fa':'ú','\\u00d1':'Ñ','\\u00f1':'ñ', '\\u00dc':'Ü', '\\u00fc':'ü','\\u0022':'"','\\u0027':'\''}
            for c in charser:texting = texting.replace(c,charser[c])
            patt = re.compile(u'(\\\\u+\w{4})', re.MULTILINE | re.IGNORECASE | re.DOTALL)
            texting = patt.sub('', texting)
    
        return texting



    def cognitiveText(self, metadata):
       
        self.csvData = self.csvData[[0,1]]   
    
        X_train = self.csvData['texto']
        y_train = self.csvData['polaridad']
        
        classifier_Ridge = Pipeline([
            ('vectorizer', CountVectorizer()),
            ('tfidf', TfidfTransformer()),
            ('clf', OneVsRestClassifier(RidgeClassifier()))])
    
        classifier_Ridge.fit(X_train, y_train)
        pred_test = classifier_Ridge.predict(metadata)
        
        
        return pred_test


    def is_json(self, myjson):
        try:
            json_object = json.loads(myjson)
        except ValueError:
            return False
        return True

        
    def getSentiment(self, datax):
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
                    jsBody = self.clearData(jsBody)
                    gBody.append(jsBody)
                    jSentiment = self.cognitiveText(gBody)
                         
                    
                
                if jSentiment:
                    richSent = jSentiment[0]
    
            except Exception as e:
                richSent = "NEUTRAL"
                print(e)
                self.getSentiment(richJson)	
            

        #jSentiment = richSent
        
	#print richSent
        return richSent
        
        
    def regenerateData(self, jdata):
        #print jdata
        jsTweet = json.loads(jdata)
        
        thesentiment = self.getSentiment(jdata)
 	#jsTweet["polarizacion"] = str(thesentiment)
        #print thesentiment
        return jsTweet
    

