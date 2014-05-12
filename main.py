import common, blog, user, jsonHandler, webapp2

class MainPage(common.Handler):
    def get(self):
        self.render("signup.html")

app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/blog', blog.BlogHandler),
  ('/newpost', blog.NewPostHandler),
  ('/blog/(\d+)', blog.PostHandler),
  ('/signup', user.SignupHandler),
  ('/login', user.LoginHandler),
  ('/logout', user.LogoutHandler),
  ('/unit3/welcome', user.WelcomeHandler)
  ('/blog/.json', json.JsonBlogHandler)
  ], debug = True)