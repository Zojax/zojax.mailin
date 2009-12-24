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

$Id$
"""

import re, os
import logging, sys

import email
from email.Header import decode_header, make_header


def log(msg='', subsystem='zojax.mailin'):
    log = logging.getLogger(subsystem)
    log.log(logging.INFO, msg)

def log_exc(msg='', subsystem='zojax.mailin'):
    log = logging.getLogger(subsystem)
    log.log(logging.ERROR, msg, exc_info=sys.exc_info())


def log_error(msg='', subsystem='zojax.mailin'):
    log = logging.getLogger(subsystem)
    log.log(logging.ERROR, msg)


def wrap_filename(f_name):
    dir, f_name = os.path.split(f_name)
    f_name = f_name.split('\\')[-1].split('/')[-1]
    for key in '~,\'':
        try:
            f_name = f_name.replace(key, '_')
        except:
            pass
    return f_name


def getLoads(message, number=None):
    lst = []
    msgs = message.get_payload()
    type = message.get_content_type()
    if type == 'application/octet-stream' :
        lst.append(msgs)
        return lst

    for msg in msgs :
        if msg.is_multipart() :
            loads = getLoads(msg)
            lst = lst + loads
        else:
            lst.append(msg)
    if number != None :
        return lst[number]
    return lst


def getSubject(msg):
    """ get mail subject """
    return make_header(
        decode_header(msg.get('Subject').strip())).__unicode__()


def getParsedBody(msg):
    """ return parsed body """
    def conv(st, cs):
        charsets = ['koi8-r', 'cp1251', 'iso-8859-1']
        if cs is not None:
            charsets = [cs] + charsets

        for cs in charsets:
            try:
                return unicode(st, cs, 'replace')
            except:
                pass
        return unicode(st)

    if msg.is_multipart():
        for msg in getLoads(msg):
            type = msg.get_content_type()
            if type == None :
                type = 'text/plain'
            if type == 'text/plain':
                return conv(msg.get_payload(decode=1),
                            msg.get_content_charset()), 'text/plain'
            if type == 'text/html':
                return conv(msg.get_payload(decode=1),
                            msg.get_content_charset()), 'text/html'
        return '', ''
    else:
        st = msg.get_payload(decode=1)
        if st is None:
            return '', 'text/plain'

        st = conv(st, msg.get_content_charset())

        st = email.quopriMIME.decode(st)

        if msg.get_content_type() == 'text/html':
            return st, 'text/html'
        else:
            return st, 'text/plain'


# getAttachments returns a list containing information on the
# attachments for a given message. Every list entry is a tuple
# containing the attachment's filename, data, content type and
# content-disposition in the original message.
def getAttachments(msg):
    """ return attachment name, data, type and content-disposition """

    # attachments can only be contained in multipart messages
    if (msg.is_multipart()):
        attachments = []

        for msg in getLoads(msg):
            # if a part of the message has the Content-Disposition set
            # it can be an attachment. We also save the original content
            # disposition information.
            if (msg.has_key('Content-Disposition')):
                _filename = msg.get_filename()
                if _filename is None:
                    _filename = u''
                else:
                    _filename = wrap_filename(unicode(_filename))
                _data = msg.get_payload(decode=True)
                _type = unicode(msg.get_content_type())
                _disposition = unicode(
                    msg.get('Content-Disposition')).split (';', 1)

                attachments.append((_filename, _data, _type, _disposition[0]))

        return attachments
    else:
        return ()


# from SecureMailHost
EMAIL_RE = re.compile(r"^(\w&.%#$&'\*+-/=?^_`{}|~]+!)*[\w&.%#$&'\*+-/=?^_`{}|~]+@(([0-9a-z]([0-9a-z-]*[0-9a-z])?\.)+[a-z]{2,6}|([0-9]{1,3}\.){3}[0-9]{1,3})$", re.IGNORECASE)

# from CMFDefault.RegistrationTool
_TESTS = ( ( re.compile("^[0-9a-zA-Z\.\-\_\+\']+\@[0-9a-zA-Z\.\-]+$")
           , True
           , "Failed a"
           )
         , ( re.compile("^[^0-9a-zA-Z]|[^0-9a-zA-Z]$")
           , False
           , "Failed b"
           )
         , ( re.compile("([0-9a-zA-Z_]{1})\@.")
           , True
           , "Failed c"
           )
         , ( re.compile(".\@([0-9a-zA-Z]{1})")
           , True
           , "Failed d"
           )
         , ( re.compile(".\.\-.|.\-\..|.\.\..|.\-\-.")
           , False
           , "Failed e"
           )
         , ( re.compile(".\.\_.|.\-\_.|.\_\..|.\_\-.|.\_\_.")
           , False
           , "Failed f"
           )
         , ( re.compile(".\.([a-zA-Z]{2,3})$|.\.([a-zA-Z]{2,4})$")
           , True
           , "Failed g"
           )
         )

def checkEmail( address ):
    if EMAIL_RE.search(address) == None:
        return False

    for pattern, expected, message in _TESTS:
        matched = pattern.search( address ) is not None
        if matched != expected:
            return False
    return True
