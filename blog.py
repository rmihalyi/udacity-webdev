import common
from google.appengine.ext import db

### Blog table
class Blog(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class PostHandler(common.Handler):
    def render_post(self, pid):
        post = Blog.get_by_id(int (pid))
        self.render("post.html", subject=post.subject, content=post.content, date=post.created.date())
    
    def get(self, pid):
        self.render_post(pid)

### Handles the front page of the blog
class BlogHandler(common.Handler):
  def render_front(self):
      posts = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")
      self.render("blog.html", posts=posts)
  
  def get(self):
      self.render_front()

### Handles the functionality for posting a new blog post
class NewPostHandler(common.Handler):
  def render_newpost(self, subject="", content="", error=""):
      self.render("newpost.html", subject=subject, content=content, error=error)

  def get(self):
      self.render_newpost()

  def post(self):
    subject = self.request.get("subject")
    content = self.request.get("content")
    error = ""

    if subject and content:
        b = Blog(subject = subject, content = content)
        b.put()
        #self.render_newpost("", "", b.key().id())
        self.redirect("/blog/" + str(b.key().id()))
    else:
        error = "Both the subject and content forms should be filled"
        self.render_newpost(subject, content, error)
