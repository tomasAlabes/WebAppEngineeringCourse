import hmac

secret = "pincha"

class CookieManager():

    @staticmethod
    def set_secure_cookie(cookieName, val, response):
        cookie_val = CookieManager.make_secure_val(val)
        response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (cookieName, cookie_val))

    @staticmethod
    def set_empty_cookie(response):
        response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    @staticmethod
    def read_secure_cookie(cookieName, request):
        cookie_val = request.cookies.get(cookieName)
        return cookie_val and CookieManager.check_secure_val(cookie_val)

    @staticmethod
    def make_secure_val(val):
        return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

    @staticmethod
    def check_secure_val(secure_val):
        val = secure_val.split('|')[0]
        if secure_val == CookieManager.make_secure_val(val):
            return val
