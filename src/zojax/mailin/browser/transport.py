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
from email import message_from_string

from zope.component import getUtility
from zojax.mailin.utils import log, log_exc
from zojax.mailin.interfaces import IMailIn, MailInException


class MailInTransport(object):

    def __call__(self, *args, **kw):
        request = self.request

        mail = request.get('mail')
        if not mail:
            return 'failed'

        # convert mail
        try:
            msg = message_from_string(mail.encode('utf-8'))
        except:
            log_exc('Error parsing email')
            return 'failed'

        configlet = getUtility(IMailIn)

        # check message for loops, wrong mta hosts, etc
        try:
            configlet.checkMessage(msg, mail, request)
        except MailInException, msg:
            log(str(msg))
            return 'failed'

        # process message
        try:
            configlet.process(msg)
        except MailInException, msg:
            log(str(msg))
            return 'failed'

        return 'success'
