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
from email.Utils import parseaddr

from zope import interface
from zope.component import queryUtility

from interfaces import IMailIn, IMailInDestination
from interfaces import MailInException, CheckMessageException


class MailInConfiglet(object):
    interface.implements(IMailIn)

    def process(self, message):
        if not message.has_key('To'):
            raise MailInException("Can't find destination location")

        # get destination address
        to_hdr = []
        for hdr in message['To'].split(','):
            to_hdr.append(parseaddr(hdr)[1].lower())

        # find destination
        destinations = []
        for to in to_hdr:
            destination = queryUtility(IMailInDestination, to)
            if destination is not None:
                destinations.append(destination)

        if not destinations:
            raise MailInException(
                "Can't find destination location: %s"%message['To'])

        # deliver
        for destination in destinations:
            destination.process(message)

    def checkMessage(self, message, raw_message, request):
        if self.max_size and (len(raw_message) > self.max_size):
            raise CheckMessageException(
                'Max size exceeded %s' % len(raw_message))

        # Check for MTA IP
        mtahosts = self.mta_hosts
        if mtahosts:
            if 'HTTP_X_FORWARDED_FOR' in request:
                REMOTE_IP = request['HTTP_X_FORWARDED_FOR']
            elif 'REMOTE_ADDR' in request:
                REMOTE_IP = request['REMOTE_ADDR']
            else:
                REMOTE_IP = None

            if REMOTE_IP and REMOTE_IP not in mtahosts:
                raise CheckMessageException(
                    'Host %s is not allowed' % (REMOTE_IP))

        # check x-mailer
        mailer = 'zojax.mailer'
        if message.get('X-Mailer') == mailer:
            raise CheckMessageException('Loop detected')
