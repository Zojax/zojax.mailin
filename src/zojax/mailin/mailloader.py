#!/usr/bin/env python
##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
Aliases:

(address): |"python path-to-script/mailloader.py http://host-name"


$Id$
"""
import sys, urllib, traceback

MAXSIZE = 0
HOSTNAME = u'%(HOSTNAME)s'


def main(argv):
    file = open('/tmp/mailtransport.log', 'ab')

    if len(argv) > 1:
        host = argv[1]
    else:
        host = HOSTNAME

    url = host+'/mailinTransport'

    print >> file, url

    email = sys.stdin.read()

    print >> file, email

    if (MAXSIZE>0) and (len(email) > MAXSIZE):
        raise Exception('Maximum size exceeded.')

    try:
        t = urllib.urlopen(url, urllib.urlencode({'mail': email}))
        print >> file, t.read()
    except:
        traceback.print_exc(file=file)
        pass

    print >> file, 'done -----------------'

if __name__ == '__main__':
    main(sys.argv)
