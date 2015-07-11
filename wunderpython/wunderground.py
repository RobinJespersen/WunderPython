# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2015 Robin Jespersen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import json, urllib, datetime

from wunderpython import stupidcache as cache

class Wunderground:
    API_AUTOCOMPLETE_URL = "http://autocomplete.wunderground.com/aq"
    API_BASE_URL = "http://api.wunderground.com/api/"
    API_FORMAT = "json"
    API_KEY = None
    
    CACHE_PATH = './cache'
    
    def __init__(self, api_key, cache_path=CACHE_PATH):
        self.API_KEY= api_key
        self.CACHE_PATH = cache_path
    
    def __getitem__(self, key):
        if type(key) is str:
            data = json.loads(cache.urlopen(self.API_AUTOCOMPLETE_URL+"?query="+urllib.quote(key), self.CACHE_PATH))['RESULTS']
            if len(data) != 1:
                raise KeyError
            return Location(data[0], self);
                
        elif type(key) is tuple:
            results = []
            for city in key:
                data = json.loads(cache.urlopen(self.API_AUTOCOMPLETE_URL+"?query="+urllib.quote(city), self.CACHE_PATH))['RESULTS']
                if len(data) != 1:
                    raise KeyError
                results.append(Location(data[0], self));
            return results
    
    def search(self, q):
        data = json.loads(cache.urlopen(self.API_AUTOCOMPLETE_URL+"?query="+urllib.quote(q), self.CACHE_PATH))['RESULTS']
        result=[]
        for d in data:
            result.append(d['name'])
        return result


class Location:
    def __init__(self, data, api):
        self.__dict__ = data
        self.API = api
        self.history = History(self.l, self.API)
    
    def __getattr__(self, key):
        if key in ['alerts', 'almanac', 'astronomy', 'conditions', 'forecast', 'forecast10day', 'hourly', 'hourly10day', 'rawtide', 'satellite', 'tide', 'webcams']:
            data = json.loads(cache.urlopen(self.API.API_BASE_URL+self.API.API_KEY +"/"+key+self.l+"."+self.API.API_FORMAT))
            if 'response' in data and 'error' in data['response'] and data['response']['error']['type'] == 'keynotfound':
                raise KeyError('keynotfound')
            if key in ['forecast10day']:
                return data['forecast']
            if key in ['astronomy']:
                return data
            if key in ['conditions']:
                return data['current_observation']
            if key in ['hourly', 'hourly10day']:
                return data['hourly_forecast']
            return data[key]
        else:
            raise AttributeError

class History:
    def __init__(self, link, api):
        self.l = link
        self.API = api
        
    def __getitem__(self, key):
        if type(key) is str:
            try:
                day = datetime.datetime.strptime(key, "%Y.%m.%d")
                return self._getWeatherForDay(day)
            except ValueError:
                raise KeyError
        elif type(key) is slice:
            try:
                start = datetime.datetime.strptime(key.start, "%Y.%m.%d")
                stop = datetime.datetime.strptime(key.stop, "%Y.%m.%d")
                result = []
                for day in self._daterange(start, stop):
                    result.append(self._getWeatherForDay(day))
                
                return result
            except ValueError:
                raise KeyError
        elif type(key) is tuple:
            result = []
            for d in key:
                try:
                    day = datetime.datetime.strptime(d, "%Y.%m.%d")
                except ValueError:
                    raise KeyError
                result.append(self._getWeatherForDay(day))
            return result
            
    def _daterange(self, startDate, endDate):
        for n in range(int ((endDate - startDate).days)):
            yield startDate + datetime.timedelta(n)
    
    def _getWeatherForDay(self, day):
        now = datetime.datetime.now()
        if datetime.datetime(day.year, day.month, day.day) > now:
            raise KeyError
            
        if day.year == now.year and day.month == now.month and day.day == now.day:
            return json.loads(cache.urlopen(self.API.API_BASE_URL+self.API.API_KEY+"/history_"+datetime.datetime.strftime(day, "%Y%m%d")+self.l+"."+self.API.API_FORMAT))['history']
        else:
            return json.loads(cache.urlopen(self.API.API_BASE_URL+self.API.API_KEY+"/history_"+datetime.datetime.strftime(day, "%Y%m%d")+self.l+"."+self.API.API_FORMAT, self.API.CACHE_PATH))['history']
    
