import common
from google.appengine.ext import db

def encodeBlog(obj):
    if isinstance(obj, Blog):
        return obj.__dict__
    return obj

### Handles the front page of the blog
class BlogHandler(common.Handler):
  def render_front(self):
      posts = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")
      posts = list(posts)
      self.render_json(posts.dumps(posts, default=encodeBlog))
  
  def get(self):
      self.render_front()