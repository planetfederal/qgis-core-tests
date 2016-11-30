from builtins import object
# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#

from qgis.core import QgsMessageLog

class CoreTestsPlugin(object):

    def __init__(self, iface):
        self.iface = iface
        try:
            from coretests.tests import testerplugin
            from qgistester.tests import addTestModule
            addTestModule(testerplugin, "Core Tests")
        except Exception as e:
            QgsMessageLog.logMessage("Tests could not be loaded! %s" % e,
                                     level=QgsMessageLog.CRITICAL)

    def initGui(self):
        pass

    def unload(self):
        pass
