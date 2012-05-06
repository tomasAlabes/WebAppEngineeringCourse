__author__ = 'Tomi'

import webapp2
import re

html = """
<!DOCTYPE html>

<html>
  <head>
    <title>Sign Up</title>
    <style type="text/css">
      .label {text-align: right}
      .error {color: red}
    </style>

  </head>

  <body>
    <h2>Signup</h2>
    <form method="post">
      <table>
        <tr>
          <td class="label">
            Username
          </td>
          <td>
            <input type="text" name="username" value="%(username)s">
          </td>
          <td class="error">

          </td>
        </tr>

        <tr>
          <td class="label">
            Password
          </td>
          <td>
            <input type="password" name="password" value="%(password)s">
          </td>
          <td class="error">

          </td>
        </tr>

        <tr>
          <td class="label">
            Verify Password
          </td>
          <td>
            <input type="password" name="verify" value="%(verify)s">
          </td>
          <td class="error">

          </td>
        </tr>

        <tr>
          <td class="label">
            Email (optional)
          </td>
          <td>
            <input type="text" name="email" value="%(email)s">
          </td>
          <td class="error">

          </td>
        </tr>
      </table>

      <input type="submit">
    </form>
  </body>

</html>
"""

USER_RE = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
PASSWORD_RE = re.compile('^.{3,20}$')
EMAIL_RE = re.compile('^[\S]+@[\S]+\.[\S]+$')

class SignUpHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(html)
        #% {'usernameError': '',
           #'passwordError':'',
           #'emailError':''}
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        is_valid_username = valid_username(username)
        is_valid_password = valid_password(password)
        is_valid_email = valid_email(email)
        if is_valid_username and is_valid_password and (is_valid_email or email == ''):
            if password == verify:
                self.redirect('/welcome?username='+username)
        else:
            #values = {'username': username, 'email': email}
            #errorMsg = 'Thats not a valid '
            #if not is_valid_username:
            #    values['usernameError'] = (errorMsg + 'username')
            #elif not is_valid_password:
            #    values['passwordError'] = (errorMsg + 'password')
            #else:
            #    values['emailError'] = (errorMsg + 'email')

            self.response.out.write(html % {"username": username, "email": email})

def valid_username(username):
    return USER_RE.match(username)

def valid_email(email):
    return EMAIL_RE.match(email)

def valid_password(password):
    return PASSWORD_RE.match(password)


welcomeHtml = """
<!DOCTYPE html>

<html>
  <head>
    <title>Welcome!</title>
  </head>
  <body>
    <h2> Welcome %(username)s !</h2>

  </body>

</html>
"""

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        self.response.out.write(welcomeHtml % {'username' : username})

