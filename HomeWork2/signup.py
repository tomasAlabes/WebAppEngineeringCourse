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
          <td class="error">%(err_user)s

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
            %(err_passw1)s
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
            %(err_passw2)s
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
            %(err_email)s
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
    def write_form(self, username="", email="", err_user="", err_passw1="", err_passw2="", err_email=""):
        self.response.out.write(html %{"username": username, "password": "", "verify": "", "email": email, "err_user":err_user, "err_passw1":err_passw1, "err_passw2":err_passw2, "err_email":err_email })

    def get(self):
       self.write_form()

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        err_user = ""
        if not USER_RE.match(username):
            err_user = "That's not a valid username."

        err_passw1 = ""
        err_passw2 = ""
        if len(password)==0 or not PASSWORD_RE.match(password):
            err_passw1 = "Type a password"
        elif password != verify:
            err_passw2 = "Your passwords didn't match."

        err_email = ""
        if len(email) != 0 and not EMAIL_RE.match(email):
            err_email = "That's not a valid email address"

        if err_user or err_passw1 or err_passw2 or err_email:
            self.write_form(username = username, email = email, err_user = err_user, err_passw1 = err_passw1,
                err_passw2 = err_passw2, err_email = err_email)
        else:
            self.redirect("/welcome?username=%s" % username)

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

