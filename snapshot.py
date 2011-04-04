#!/usr/bin/python
from sys import argv
from os import system

from boto.s3.connection import S3Connection
from boto.s3.key import Key


def snapshot(url_pivot, url_orig, fn, ext):
    print "Create screenshot of original"
    system("/opt/wkhtmltoimage-amd64 %s '/tmp/%s-orig.%s'" % (url_orig, fn, ext))
    print "- Create thumbnail"
    system("convert -resize 133x100 '/tmp/%s.%s' '/tmp/%s-orig_thumb.%s'" % (fn, ext, fn, ext))
    print "- Minify screenshot"
    system("mogrify -resize 1024x769 '/tmp/%s-orig.%s'" % (fn, ext))

    print "Create screenshot of pivot"
    system("/opt/wkhtmltoimage-amd64 %s '/tmp/%s.%s'" % (url_pivot, fn, ext))
    print "- Create thumbnail"
    system("convert -resize 133x100 '/tmp/%s.%s' '/tmp/%s_thumb.%s'" % (fn, ext, fn, ext))
    print "- Minify screenshot"
    system("mogrify -resize 1024x769 '/tmp/%s.%s'" % (fn, ext))

    print "Copy into s3"
    conn = S3Connection()
    bucket = conn.create_bucket('csspivot_snapshots')

    k = Key(bucket)
    k.key = "%s.%s" % (fn, ext)
    k.set_contents_from_filename("/tmp/%s.%s" % (fn, ext))

    k = Key(bucket)
    k.key = "%s_thumb.%s" % (fn, ext)
    k.set_contents_from_filename("/tmp/%s_thumb.%s" % (fn, ext))

    k = Key(bucket)
    k.key = "%s-orig.%s" % (fn, ext)
    k.set_contents_from_filename("/tmp/%s-orig.%s" % (fn, ext))

    k = Key(bucket)
    k.key = "%s-orig_thumb.%s" % (fn, ext)
    k.set_contents_from_filename("/tmp/%s-orig_thumb.%s" % (fn, ext))


if __name__ == "__main__":
    if len(argv) < 5:
        print "Use: $0 [url_pivot] [url_orig] [image-fnbase] [image-ext]"
        exit(1)

    snapshot(argv[1], argv[2], argv[3], argv[4])
