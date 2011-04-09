#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import snapshot

urls = (
    "/snap/(.*)", "snap",
    "/.*", "hello",
)

app = web.application(urls, globals())


class hello:
    def GET(self):
        return 'Hello, world!'


class snap:
    def GET(self, pivot_id):
        i = web.input()
        url = i.url
        if pivot_id and url:
            snapshot.snapshot_pivot("http://www.csspivot.com/proxy/%s" % \
                    pivot_id, url, pivot_id)
            return "https://s3.amazonaws.com/csspivot_snapshots/%s"


if __name__ == "__main__":
    #web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app.run()
