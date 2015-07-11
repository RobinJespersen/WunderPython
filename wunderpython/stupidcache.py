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

import urllib2, sha, os.path

def urlopen(url, path=False):
    if path:
        urlHash = sha.new(url).hexdigest()
        if not os.path.exists(path):
            os.makedirs(path)
        if os.path.isfile(os.path.join(path, urlHash)):
            return open(os.path.join(path, urlHash), 'r').read()
        else:
            cacheFile = open(os.path.join(path, urlHash), 'w')
            cacheFile.write(urllib2.urlopen(url).read())
            cacheFile.close()
            return open(os.path.join(path, urlHash), 'r').read()
    else:
        return urllib2.urlopen(url).read()
