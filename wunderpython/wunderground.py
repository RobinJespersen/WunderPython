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
        
    def search(self, q):
        data = json.loads(cache.urlopen(self.API_AUTOCOMPLETE_URL+"?query="+urllib.quote(q), self.CACHE_PATH))['RESULTS']
        result=[]
        for d in data:
            result.append(d['name'])
        return result



