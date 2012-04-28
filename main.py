#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi

abc = ['a','b','c','d','e','f','g','h','i','j','k',
              'l','m','n','o','p','q','r','s','t','u','v',
              'w','x','y','z']

html = """
<h1>Enter some text to ROT13</h1>
<form method="post" action="/riot13">
    <textarea name="text" cols="50" rows="7">%(rioted)s</textarea>
    <br>
    <input type="submit"/>
</form>
"""

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Hello udacity!")

class RiotHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(html % {"rioted": ''})
    def post(self):
         text = self.request.get('text')
         riotedString = riot(text)
         self.response.out.write(html % {"rioted": riotedString})

def riot(string):
    result = ""
    for letter in string:
        abcLength = len(abc)
        if letter in abc:
            ix = abc.index(letter)
            if ix != -1:
                newIx = ix + 13
                if newIx >= abcLength:
                    newIx = (newIx - abcLength)
                result += abc[newIx]
        else:
            result += letter
    escapedString = cgi.escape(result, True)
    return escapedString

def unescape(s):
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    # this has to be last:
    s = s.replace("&amp;", "&")
    return s

app = webapp2.WSGIApplication([('/', MainHandler),
                                ('/rot13', RiotHandler)],
                              debug=True)
