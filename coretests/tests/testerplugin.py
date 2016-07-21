'''
Tests to ensure that a QGIS installation contains Processing dependencies
and they are correctly configured by default
'''
import unittest
import sys
from processing.algs.saga.SagaUtils import *
from processing.algs.otb.OTBUtils import *
from qgis.utils import plugins, iface
from qgis.core import *
import os
from qgistester.test import Test
from packages_tests import PackageTests
from platform_tests import TestImports, TestSupportedFormats, TestOtherCommandLineUtilities


def _loadSpatialite():
    uri = QgsDataSourceURI()
    uri.setDatabase(os.path.join(os.path.dirname(__file__), "data", "elk.sqlite"))
    schema = ''
    table = 'elk'
    geom_column = 'the_geom'
    uri.setDataSource(schema, table, geom_column)
    layer = QgsVectorLayer(uri.uri(), "test", 'spatialite')
    assert layer.isValid()
    QgsMapLayerRegistry.instance().addMapLayer(layer)

def _openDBManager():
        plugins["db_manager"].run()

def _openLogMessagesDialog():
    widgets = [el for el in iface.mainWindow().children() if el.objectName() == "MessageLog"]
    widgets[0].setVisible(True)


def _openAboutDialog():
    iface.actionAbout().trigger()

def functionalTests():
    spatialiteTest = Test("Test Spatialite. QGIS-72")
    spatialiteTest.addStep("Load Spatialite layer", _loadSpatialite)
    spatialiteTest.addStep("Open DB Manager", _openDBManager)
    spatialiteTest.addStep("Check that 'elk' layer is available in DB manager")

    aboutTest = Test("Verify dependency versions and providers in About dialog. QGIS-53")
    aboutTest.addStep("Open About dialog", _openAboutDialog)
    if sys.platform == 'darwin':
        descriptionFile = os.path.join(os.path.dirname(__file__), "data", "about.mac")
    else:
        descriptionFile = os.path.join(os.path.dirname(__file__), "data", "about.windows")
    aboutTest.addStep(descriptionFile)

    logTest = Test("Verify in-app message log has no errors for default install. QGIS-54")
    logTest.addStep("Open log messages panel", _openLogMessagesDialog)
    logTest.addStep("Review 'General' tab output. Check it has no issues", isVerifyStep = True)
    logTest.addStep("Check there are no errors in 'Plugins' tab", isVerifyStep = True)
    logTest.addStep("Check there is no 'Python warning' tab", isVerifyStep = True)
    logTest.addStep("Check there is no 'Qt' tab", isVerifyStep = True)
    logTest.addStep("Check there is no other tab", isVerifyStep = True)

    return [spatialiteTest, aboutTest, logTest]


def unitTests():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(PackageTests))
    suite.addTests(unittest.makeSuite(TestImports))
    suite.addTests(unittest.makeSuite(TestSupportedFormats))
    suite.addTests(unittest.makeSuite(TestOtherCommandLineUtilities))
    return suite
