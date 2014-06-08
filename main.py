import common, blog, user, jsonHandler, webapp2

class MainPage(common.Handler):
    def get(self):
        self.render("signup.html")

app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/blog/?(?:.json)?', blog.BlogHandler),
  ('/blog/(\d+)(?:.json)?', blog.PostHandler),
  ('/newpost', blog.NewPostHandler),
  ('/signup', user.SignupHandler),
  ('/login', user.LoginHandler),
  ('/logout', user.LogoutHandler),
  ('/unit3/welcome', user.WelcomeHandler)
  #('/blog/.json', jsonHandler.JsonBlogHandler)
  ], debug = True)