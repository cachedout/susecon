# -*- coding: utf-8 -*-
'''
A very simple engine that takes an HTTP POST
and puts a corresponding event on the Salt event
bus. Intended for demonstration purposes only.
'''

# Import Python libs
import logging
import json

# Import Tornado libs
import tornado.web

from tornado.options import define

# Import Salt events
import salt.utils.event

log = logging.getLogger(__name__)

# Set up Tornado options



def start():
    '''
    Start up the webserver
    '''
    class IndexHandler(tornado.web.RequestHandler):
        SUPPORTED_METHODS = ("CONNECT", "GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
	def set_default_headers(self):
	    log.info("setting headers!!!")
	    self.set_header("Access-Control-Allow-Origin", "*")
	    self.set_header("Access-Control-Allow-Headers", "x-requested-with, Content-Type")
	    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

        def options(self):
            self.set_status(204)
            self.finish()

        @tornado.gen.coroutine
        def get(self):
            #Optional event firing for more integration
            yield event_bus.fire_event({'headers': str(self.request.headers),
                                        'body': json.loads(self.request.body)},
                                        '/salt/engines/http',
                                        ret_future=True)
            g = __runners__['lambda_events.giphyget'](json.loads(self.request.body)['giphy_request'])

            self.write(g['url'])
            self.finish()

        #@tornado.gen.coroutine
        @tornado.web.asynchronous
        def post(self):
            #Optional event firing for more integration
        #    yield event_bus.fire_event({'headers': str(self.request.headers),
        #                                'body': json.loads(self.request.body)},
        #                                '/salt/engines/http',
         #                               ret_future=True)
            log.info(json.loads(self.request.body))
            g = __runners__['lambda_events.giphyget'](json.loads(self.request.body)['giphy_request'])
            self.write(g['url'])
            self.finish()


    log.info('Starting simple HTTP engine event service!')
#    if __opts__['__role'] == 'master':
#        log.info('Starting master event bus')
#        event_bus = salt.utils.event.get_master_event(
#                __opts__,
#                __opts__['sock_dir'],
#                listen=True)
#    else:

    log.info('Simple HTTP engine event service started!')

    log.info('Starting simple HTTP engine webserver!')
    app = tornado.web.Application([
        (r'/', IndexHandler),
        ])
    app.listen(9999)
    log.info('Simple HTTP engine webserver ready for requests!')
    
    # Start the web server!
    io_loop = tornado.ioloop.IOLoop.current()

    event_bus = salt.utils.event.get_master_event(
            __opts__,
            __opts__['sock_dir'],
            listen=True,
            io_loop=io_loop)

    io_loop.start()


