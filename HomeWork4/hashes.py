__author__ = 'Tomi'

import random
import string
import hashlib

class HashManager():

    def makeSalt(self):
        return ''.join(random.choice(string.letters) for x in xrange(5))

    def makePasswordHash(self, name, password, salt = None):
        if not salt:
            salt = self.makeSalt()
        h = hashlib.sha256(name + password + salt).hexdigest()
        return '%s,%s' % (h, salt)

    def validPassword(self, name, password, h):
        print h
        salt = h.split(',')[1]
        return h == self.makePasswordHash(name, password, salt)

    def hashString(self, string):
        return hashlib.md5(string).hexdigest()

    def makeStringHash(self, string):
        return '%s|%s' % (string, self.hashString(string))

    def validStringHash(self, hash):
        hash_split = hash.split('|')
        val = hash_split[0]
        hashVal = hash_split[1]
        if hashVal == self.hashString(val):
            return val

