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
""" Setup for zojax.mailin package

$Id$
"""
import sys, os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version='0.2.0'


setup(name = 'zojax.mailin',
      version = version,
      author = 'Nikolay Kim',
      author_email = 'fafhrd91@gmail.com',
      description = "Mail-in subsystem for zojax",
      long_description = (
          'Detailed Documentation\n' +
          '======================\n'
          + '\n\n' +
          read('CHANGES.txt')
          ),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Zope3'],
      url='http://zojax.net/',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir = {'':'src'},
      namespace_packages=['zojax'],
      install_requires = ['setuptools', 'rwproperty',
                          'zope.interface',
                          'zope.component',
                          'zope.security',
                          'zope.sendmail',
                          'zope.i18n',
                          'zope.i18nmessageid',
                          'zope.app.security',
                          'zope.app.intid',
                          'z3c.schema',
                          'zojax.mail',
                          'zojax.mailtemplate',
                          'zojax.controlpanel',
                          'zojax.widget.list',
                          'zojax.wizard',
                          'zojax.content.type',
                          'zojax.content.forms',
                          ],
      extras_require = dict(test=['zope.testing',
                                  'zope.app.testing',
                                  'zope.app.zcmlfiles',
                                  'zojax.autoinclude',
                                  'zojax.security',
                                  ]),
      include_package_data = True,
      zip_safe = False
      )
