from webapp2 import RequestHandler


class HomePage(RequestHandler):
    def get(self):
        self.response.write('Just for practice')
