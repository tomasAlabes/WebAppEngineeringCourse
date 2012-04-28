__author__ = 'Tomi'

import webapp2
import cgi

abc = ['a','b','c','d','e','f','g','h','i','j','k',
       'l','m','n','o','p','q','r','s','t','u','v',
       'w','x','y','z']

html = """
<h1>Enter some text to ROT13</h1>
<form method="post" action="/rot13">
    <textarea name="text" cols="50" rows="7">%(rioted)s</textarea>
    <br>
    <input type="submit"/>
</form>
"""

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
        isSupper = letter.isupper()
        letter = letter.lower()
        abcLength = len(abc)
        if letter in abc:
            ix = abc.index(letter)
            if ix != -1:
                newIx = ix + 13
                if newIx >= abcLength:
                    newIx = (newIx - abcLength)
                newLetter = abc[newIx]
                if isSupper:
                    newLetter = newLetter.upper()
                result += newLetter
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
