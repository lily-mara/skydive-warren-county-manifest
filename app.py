import os

import tornado.ioloop
import tornado.web
import tornado.autoreload
from tornado.options import define, options, parse_command_line

from jumprun import JumprunProApi


DROPZONE = 'skydive-warren-county'
BASE_PATH = os.path.dirname(os.path.realpath(__file__))
API = JumprunProApi(DROPZONE)


class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html')


class DepartingLoadsHandler(tornado.web.RequestHandler):
	def get(self):
		loads = API.departing_loads()
		self.finish({'loads': loads})

handlers = [
	(r'/', IndexHandler),
	(r'/api/departing', DepartingLoadsHandler),
]

settings = {
	'debug': True,
	'static_path': os.path.join(BASE_PATH, 'static'),
	'template_path': os.path.join(BASE_PATH, 'templates')
}

application = tornado.web.Application(handlers, **settings)

define(
	'port',
	help='The port that this instance of the server should listen on',
	default='8080',
	type=int,
)

if __name__ == '__main__':
	parse_command_line()
	print('Listening on port {}...'.format(options.port))

	tornado.autoreload.start()

	application.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
