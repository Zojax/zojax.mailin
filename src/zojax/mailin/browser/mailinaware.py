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
from zope import interface
from zojax.layoutform import Fields
from zojax.wizard.step import WizardStepForm
from zojax.wizard.interfaces import ISaveable
from zojax.mailin.interfaces import IMailInAwareDestination
from zojax.content.type.interfaces import IDraftedContent


class MailInAwareForm(WizardStepForm):
    interface.implements(ISaveable)

    fields = Fields(IMailInAwareDestination)

    def isAvailable(self):
        if IDraftedContent.providedBy(self.getContent()):
            return False

        return super(MailInAwareForm, self).isAvailable()
