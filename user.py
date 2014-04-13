import common, random, string, hmac, hashlib
from google.appengine.ext import db

def hash_str(s):
    return hmac.new(common.SECRET, s).hexdigest()

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val

def make_salt():
    return ''.join(random.sample(string.letters + string.digits, 10))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (h, salt)

def valid_pw(name, pw, h):
    salt = h.split('|')[1]
    if make_pw_hash(name, pw, salt) == h:
        return True

### User table
class User(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

### Handles the signup functionality
class SignupHandler(common.Handler):
    def render_signup(self, username="", email="", user_error="", pass_error="", verify_error="", email_error=""):
        self.render("signup.html", username=username, email=email, user_error=user_error, pass_error=pass_error, verify_error=verify_error, email_error=email_error)

    def get(self):
        self.render_signup()

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        user_error = ""
        pass_error = ""
        verify_error = ""
        email_error = ""
        if not common.valid_username(username):
            user_error = "That's not a valid username."
        if not common.valid_password(password):
            pass_error = "That wasn't a valid password."
        if not password == verify:
            verify_error = "Your passwords didn't match."
        if email and not common.valid_email(email):
            email_error = "That's not a valid email."
        elif not email:
            email_error = ""

        self.render_signup(username, email, user_error, pass_error, verify_error, email_error)

        if user_error is "" and pass_error is "" and verify_error is "" and email_error is "":
            u = User(username = username, password = make_pw_hash(username, password))
            u.put()
            set_cookie_val = "user_id=%s; Path=/" % make_secure_val(str(u.key().id()))
            self.response.headers.add_header('Set-Cookie', set_cookie_val)
            self.redirect("/unit3/welcome")

### Handles the welcome screen
class WelcomeHandler(common.Handler):
    def get(self):
        common.logging.debug('Welcome handler')
        cookie_str = self.request.cookies.get("user_id")
        if cookie_str:
          cookie_val = check_secure_val(cookie_str)
          if cookie_val:
              # cookie_val is user_id
              user = User.get_by_id(int (cookie_val))
              self.write("<h1>Welcome, " + user.username + "!</h1>")
        else:
          self.redirect("/signup")