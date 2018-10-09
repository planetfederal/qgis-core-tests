# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#

from builtins import object

class CoreTestsPlugin(object):

    def __init__(self, iface):
        self.iface = iface

        try:
            from coretests.tests import testerplugin
            from qgistester.tests import addTestModule
            addTestModule(testerplugin, "Core Tests")
        except Exception as e:
            raise
            pass

    def initGui(self):
        pass

    def unload(self):
        pass
