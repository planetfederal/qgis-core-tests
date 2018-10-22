'''
Tests to ensure that a QGIS installation contains Processing dependencies
and they are correctly configured by default
'''

import os
import sys
import unittest

from qgis.utils import plugins, iface
from qgis.core import QgsDataSourceUri, QgsVectorLayer, QgsRasterLayer, QgsProject

from coretests.tests.packages_tests import PackageTests
from coretests.tests.platform_tests import TestImports, TestSupportedFormats, TestOtherCommandLineUtilities

testPath = os.path.dirname(__file__)

TEST_WCS_URL = "TEST_WCS_URL"
TEST_WFS_URL = "TEST_WFS_URL"

def _loadSpatialite():
    uri = QgsDataSourceUri()
    uri.setDatabase(os.path.join(os.path.dirname(__file__), "data", "elk.sqlite"))
    schema = ''
    table = 'elk'
    geom_column = 'the_geom'
    uri.setDataSource(schema, table, geom_column)
    layer = QgsVectorLayer(uri.uri(), "test", 'spatialite')
    assert layer.isValid()
    QgsProject.instance().addMapLayer(layer)

def _openDBManager():
    plugins["db_manager"].run()

def _openLogMessagesDialog():
    widgets = [el for el in iface.mainWindow().children() if el.objectName() == "MessageLog"]
    widgets[0].setVisible(True)

def _openAboutDialog():
    iface.actionAbout().trigger()

def _loadWcs():
    uri.setParam('url', os.getenv(TEST_WCS_URL))
    uri.setParam("identifier", "testlayer")
    layer = QgsRasterLayer(str(uri.encodedUri()), 'testlayer', 'wcs')
    QgsProject.instance().addLayer(layer)

def _modifyAndLoadWfs():
    url = os.getenv(TEST_WFS_URL)
    uri = "%s?typename=union&version=1.0.0&request=GetFeature&service=WFS" % url
    layer = QgsVectorLayer(uri, "testlayer", "WFS")
    featureCount = layer.featureCount()
    featureid = list(layer.getFeatures())[0].id()
    layer.startEditing()    
    layer.deleteFeature(featureid)
    layer.commitChanges()
    layer = QgsVectorLayer(uri, "testlayer", "WFS")
    assert layer.featureCount() == featureCount - 1
    QgsProject.instance().addLayer(layer)

def functionalTests():
    try:
        from qgistester.test import Test
    except:
        return []

    spatialiteTest = Test("Test Spatialite. QGIS-72")
    spatialiteTest.addStep("Load Spatialite layer",
                           prestep=lambda:_loadSpatialite())
    spatialiteTest.addStep("Open DB Manager",
                           prestep=lambda:_openDBManager())
    spatialiteTest.addStep("Check that 'test' layer is available "
                           "in DB manager, in 'Virtual layers/QGIS layers'",
                           isVerifyStep=True)

    aboutTest = Test("Verify dependency versions and providers in About dialog. QGIS-53")
    aboutTest.addStep("Open About dialog",
                      prestep=lambda:_openAboutDialog())
    if sys.platform == 'darwin':
        filePath = os.path.join(testPath, "data", "about.mac")
    else:
        filePath = os.path.join(testPath, "data", "about.windows")
    with open(filePath) as f:
        content = f.readlines()
    data = ""
    for line in content:
        data += "<p>{}</p>".format(line)
    aboutTest.addStep("Verify that content of the About dialog matches"
                      "following data\n{}\n\n".format(data),
                      isVerifyStep=True)

    logTest = Test("Verify in-app message log has no errors for default install. QGIS-54")
    logTest.addStep("Open log messages panel",
                    prestep=lambda:_openLogMessagesDialog())
    logTest.addStep("Review 'General' tab output. Check it has no issues",
                    isVerifyStep=True)
    logTest.addStep("Check there are no errors in 'Plugins' tab",
                    isVerifyStep=True)
    logTest.addStep("Check there are no errors in 'Qt' tab",
                    isVerifyStep=True)

    wcsTest = Test("Test WCS")
    wcsTest.addStep("Load WCS layer",
                           prestep=lambda:_loadWcs())
    wcsTest.addStep("Check that 'test' layer is available in QGIS project",
                           isVerifyStep=True)

    wfsTest = Test("Test WFS")
    wfsTest.addStep("Modify and load WFS layer",
                           prestep=lambda:_modifyAndLoadWfs())
    wfsTest.addStep("Check that 'test' layer is available in QGIS project",
                           isVerifyStep=True)

    return [spatialiteTest, logTest, aboutTest, wcsTest, wfsTest]

def settings():
    return  {"TEST_WCS_URL": TEST_WCS_URL,
             "TEST_WFS_URL": TEST_WFS_URL}

def unitTests():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(PackageTests))
    suite.addTests(unittest.makeSuite(TestImports))
    suite.addTests(unittest.makeSuite(TestSupportedFormats))
    suite.addTests(unittest.makeSuite(TestOtherCommandLineUtilities))
    return suite


def run_all():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(unitTests())
