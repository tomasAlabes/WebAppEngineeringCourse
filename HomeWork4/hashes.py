__author__ = 'Tomi'

import random
import string
import hashlib

class HashManager():

    @classmethod
    def make_salt(cls, length = 5):
        return ''.join(random.choice(string.letters) for x in xrange(length))

    @classmethod
    def make_pw_hash(cls, name, pw, salt = None):
        if not salt:
            salt = HashManager.make_salt()
        h = hashlib.sha256(name + pw + salt).hexdigest()
        return '%s,%s' % (salt, h)

    @classmethod
    def valid_pw(cls, name, password, h):
        salt = h.split(',')[0]
        return h == HashManager.make_pw_hash(name, password, salt)