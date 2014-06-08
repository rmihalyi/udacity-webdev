import common
from google.appengine.ext import db

class PostHandler(common.Handler):
    def render_post(self, pid):
        post = common.Blog.get_by_id(int (pid))
        if not post:
            self.error(404)
            return
        if self.format == 'html':
            self.render("post.html", subject=post.subject, content=post.content, date=post.created.date())
        else:
            self.render_json(post.as_dict())
    
    def get(self, pid):
        self.render_post(pid)

### Handles the front page of the blog
class BlogHandler(common.Handler):
    def render_front(self):
        posts = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")
        if self.format == 'html':
            self.render("blog.html", posts=posts)
        else:
            return self.render_json([p.as_dict() for p in posts])
    
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
            b = common.Blog(subject = subject, content = content)
            b.put()
            self.redirect("/blog/" + str(b.key().id()))
        else:
            error = "Both the subject and content forms should be filled"
            self.render_newpost(subject, content, error)
