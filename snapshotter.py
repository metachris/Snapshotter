#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
from snapshot import snapshot

urls = (
    "/.*", "hello",
    "/snap/(.*)", "snap",
)

app = web.application(urls, globals())


class hello:
    def GET(self):
        return 'Hello, world!'


class snap:
    def GET(self, pivot_id):
        if pivot_id:
            snapshot("http://www.csspivot.com/%s" % pivot_id, "http://www.csspivot.com/%s" % pivot_id, pivot_id, "png")
        return 'Hello, world!'


if __name__ == "__main__":
    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app.run()
