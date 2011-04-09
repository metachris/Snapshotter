#!/usr/bin/python
from sys import argv
from os import system

from boto.s3.connection import S3Connection
from boto.s3.key import Key

ext = "png"
ext_thumb = "gif"


def snapshot(url, fn, s3bucket=None):
    print "Capture %s" % url
    system("/opt/wkhtmltoimage-amd64 --crop-h 1024 %s '/tmp/%s.%s'" % (url, fn, ext))

    print "- Create thumbnail"
    system("convert -resize 156x156 '/tmp/%s.%s' '/tmp/%s_thumb.%s'" % (fn, ext, fn, ext_thumb))

    print "- Shrink original"
    system("mogrify -resize 1024x1024 '/tmp/%s.%s'" % (fn, ext))

    if not s3bucket:
        return

    print "- Move into s3 bucket"

    k = Key(s3bucket)
    k.key = "%s.%s" % (fn, ext)
    k.set_contents_from_filename("/tmp/%s.%s" % (fn, ext))
    k.set_acl('public-read')

    k = Key(s3bucket)
    k.key = "%s_thumb.%s" % (fn, ext_thumb)
    k.set_contents_from_filename("/tmp/%s_thumb.%s" % (fn, ext_thumb))
    k.set_acl('public-read')

    system("rm /tmp/%s.%s" % (fn, ext))
    system("rm /tmp/%s_thumb.%s" % (fn, ext_thumb))


def snapshot_pivot(url_pivot, url_orig, fn):
    conn = S3Connection()
    bucket = conn.create_bucket('csspivot_snapshots')

    snapshot(url_pivot, fn, bucket)
    snapshot(url_orig, "%s-orig" % fn, bucket)


if __name__ == "__main__":
    if len(argv) < 4:
        print "Use: $0 [url_pivot] [url_orig] [image-fnbase]"
        exit(1)

    snapshot_pivot(argv[1], argv[2], argv[3])
