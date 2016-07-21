# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#

class CoreTestsPlugin:

    def __init__(self, iface):
        self.iface = iface
        try:
            from tests import testerplugin
            from qgistester.tests import addTestModule
            addTestModule(testerplugin, "Core Tests")
        except:
            pass


    def initGui(self):
        pass

    def unload(self):
        pass
