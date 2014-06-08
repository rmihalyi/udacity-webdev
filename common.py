import os, re, hmac, random, string, webapp2, logging, jinja2, hashlib, json, logging
from google.appengine.ext import db

### template helpers
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

### Main handler
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_json(self, obj):
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.write(json.dumps(obj))

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        if self.request.url.endswith('.json'):
            self.format = 'json'
        else:
            self.format = 'html'


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
    return EMAIL_RE.match(email)

SECRET = ''.join(random.sample(string.ascii_letters + string.digits, 10))

def encode_blog(obj):
    if isinstance(obj, Blog):
        return obj.__dict__
    return obj

### Blog table
class Blog(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

    def as_dict(self):
        time_format = '%c'
        d = {'subject': self.subject,
             'content': self.content,
             'created': self.created.strftime(time_format)}
        return d