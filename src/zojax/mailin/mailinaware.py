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
import copy
from persistent import Persistent
from rwproperty import getproperty, setproperty
from email.Utils import parseaddr

from zope import interface, component
from zope.proxy import removeAllProxies
from zope.component import getSiteManager, getUtility, queryUtility
from zope.annotation.interfaces import IAnnotations
from zope.app.container.interfaces import IObjectRemovedEvent
from zope.app.security.interfaces import PrincipalLookupError
from zope.app.security.interfaces import IUnauthenticatedPrincipal
from zope.publisher.browser import TestRequest
from zope.security.management import \
    queryInteraction, endInteraction, newInteraction, restoreInteraction

from zojax.mail.utils import getPrincipalByEMail

from utils import log_exc
from interfaces import MailInException
from interfaces import IRecipient, IAnonymousSupport
from interfaces import IMailInAware, IMailInDestination, IMailInAwareDestination

KEY = 'zojax.mailin.main-in-aware'


class MailInAwareDestination(Persistent):
    interface.implements(IMailInAwareDestination)

    def __init__(self, context):
        self.context = context

    def register(self):
        if not self.address:
            return

        if queryUtility(IMailInDestination, self.address) is not None:
            raise MailInException(
                'Mail-in email address already in use: %s'%self.address)
        getSiteManager().registerUtility(self, IMailInDestination, self.address)

    def unregister(self):
        getSiteManager().unregisterUtility(
            self, IMailInDestination, self.address)

    @getproperty
    def enabled(self):
        return self.__dict__.get('enabled', False)

    @setproperty
    def enabled(self, value):
        if value:
            self.register()
        else:
            self.unregister()

        self.__dict__['enabled'] = value

    @getproperty
    def address(self):
        return self.__dict__.get('address', u'')

    @setproperty
    def address(self, value):
        if self.enabled:
            self.unregister()
            self.__dict__['address'] = value
            self.register()
        else:
            self.__dict__['address'] = value

    def process(self, message):
        recipient = IRecipient(self.context, None)
        if recipient is None:
            raise MailInException('Recipent not found.')

        # find principal
        from_hdr = parseaddr(message['From'])[1].lower()
        try:
            principal = getPrincipalByEMail(from_hdr)
        except PrincipalLookupError:
            if IAnonymousSupport.providedBy(recipient):
                principal = getUtility(IUnauthenticatedPrincipal)
            else:
                # member not found
                raise MailInException('Member not found: %s'%from_hdr)

        # set security context
        interaction = queryInteraction()
        if interaction is not None:
            request = copy.copy(interaction.participations[0])
        else:
            request = TestRequest()

        request.setPrincipal(principal)
        request.interaction = None

        endInteraction()
        newInteraction(request)

        # deliver message
        try:
            recipient.process(message)
        except:
            log_exc()

        # restore old security context
        restoreInteraction()


@component.adapter(IMailInAware)
@interface.implementer(IMailInAwareDestination)
def getMailInDestination(context):
    annotation = IAnnotations(removeAllProxies(context))

    destination = annotation.get(KEY)
    if destination is None:
        destination = MailInAwareDestination(removeAllProxies(context))
        annotation[KEY] = destination

    return destination


@component.adapter(IMailInAware, IObjectRemovedEvent)
def objectRemovedEvent(object, ev):
    IMailInAwareDestination(removeAllProxies(object)).enabled = False
