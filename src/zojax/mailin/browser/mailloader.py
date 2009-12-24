##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
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

$Id$
"""
import os.path
from zope.traversing.browser import absoluteURL
from zope.app.component.hooks import getSite

mailloaderFile = os.path.join(os.path.dirname(__file__), '..', 'mailloader.py')


class MailloaderScript(object):

    def __call__(self, *args, **kw):
        request = self.request
        response = request.response

        response.setHeader(
            'Content-Disposition','attachment; filename="mailloader.py"')

        data = open(mailloaderFile, 'rb').read()

        return data%{'HOSTNAME': absoluteURL(getSite(), request)}
