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
from zope import interface, schema
from zope.i18nmessageid import MessageFactory
from z3c.schema.email import RFC822MailAddress
from zojax.widget.list import SimpleList

_ = MessageFactory('zojax.mailin')


class MailInException(Exception):
    """ base mailin exception """


class CheckMessageException(MailInException):
    """ check mail exception """


class IMailIn(interface.Interface):
    """ mail-in configlet """

    max_size = schema.Int(
        title = _('Max size'),
        description = _('Max size for incoming emails. 0 is unlimited size.'),
        required = True,
        default = 0)

    mta_hosts = SimpleList(
        title = _('MTA Hosts'),
        description = _('Allowed mta hosts. For allow all host remove everything from list.'),
        default = [],
        required = False)

    def process(message):
        """ process incoming message """

    def checkMessage(message, raw_text, request):
        """ check for loop, spam, etc """


class IMailInDestination(interface.Interface):
    """ mail-in destination """

    def process(message):
        """ deliver message """


class IMailInAware(interface.Interface):
    """ mailin aware destination """


class IMailInAwareDestination(IMailInDestination):
    """ mailin aware destination """

    enabled = schema.Bool(
        title = _('Enabled'),
        description = _('Enable mail-in support.'),
        default = False,
        required = False)

    address = RFC822MailAddress(
        title = _(u'Address'),
        description = _('Mail-in email address.'),
        required = False)


class IRecipient(interface.Interface):
    """ mail-in recipient """

    def process(message):
        """ process message """


class IAnonymousSupport(interface.Interface):
    """ allow anonymous mailin for recipient """
