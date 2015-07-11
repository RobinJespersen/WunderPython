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

import sys, os, shutil, unittest, urllib2
sys.path[0:0] = [os.path.join(os.path.dirname(__file__), ".."),]

from wunderpython import stupidcache
from wunderpython import wunderground

class TestStupidCache(unittest.TestCase):
    cacheFolder = './cache/folder/'
    cacheBaseFolder = './cache/'
    url = 'http://autocomplete.wunderground.com/aq'
    
    def test_not_cached_content(self):
        self.assertFalse(os.path.exists(self.cacheFolder))
        self.assertEqual(stupidcache.urlopen(self.url), urllib2.urlopen(self.url).read())
        self.assertFalse(os.path.exists(self.cacheFolder))
    
    def test_folder_creation(self):
        self.assertFalse(os.path.exists(self.cacheFolder))
        stupidcache.urlopen(self.url, self.cacheFolder)
        self.assertTrue(os.path.exists(self.cacheFolder))
        
    def test_cached_content(self):
        self.assertEqual(stupidcache.urlopen(self.url, self.cacheFolder), urllib2.urlopen(self.url).read())
        
    def tearDown(self):
        if os.path.exists(self.cacheFolder):
            shutil.rmtree(self.cacheBaseFolder)
            
class TestWunderground(unittest.TestCase):
    wg = wunderground.Wunderground('no_valid_key')
    
    def test_search(self):
        self.assertTrue(len(self.wg.search('')) == 20)
        self.assertTrue(type(self.wg.search(''))==list)
        self.assertTrue(len(self.wg.search('not a name of a place')) == 0)
        self.assertTrue(len(self.wg.search('Munich, Germany')) == 1)
        
    def test_location(self):
        self.assertEqual(self.wg['Munich, Germany'].name, 'Munich, Germany')
        self.assertEqual(type(self.wg['Munich, Germany', 'Berlin, Germany', 'Hamburg, Germany']), list)
        self.assertEqual(self.wg['Munich, Germany'].ll, '48.130001 11.700000')
        
    def test_features(self):
        for feature in ['almanac', 'astronomy', 'conditions', 'forecast', 'forecast10day', 'rawtide', 'satellite', 'tide']:
            self.assertEqual(type(getattr(self.wg['Munich, Germany'], feature)), dict)
            
        for feature in ['alerts', 'hourly', 'hourly10day', 'webcams']:
            self.assertEqual(type(getattr(self.wg['Munich, Germany'], feature)), list)
                

if __name__ == '__main__':
    unittest.main()
