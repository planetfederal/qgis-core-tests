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

from qgis.PyQt.QtNetwork import QSslCertificate

testPath = os.path.dirname(__file__)

TEST_URL = "TEST_URL"
TEST_PORTS = "TEST_PORTS"

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

def _loadTestLayer():
    pass

def _openDBManager():
    plugins["db_manager"].run()

def _openLogMessagesDialog():
    widgets = [el for el in iface.mainWindow().children() if el.objectName() == "MessageLog"]
    widgets[0].setVisible(True)

def _openAboutDialog():
    iface.actionAbout().trigger()

def _addPort(url, port):
    tokens = url.split("/")
    tokens[2] = tokens[2] + ":" + str(port).strip()
    return "/".join(tokens)

def _loadArcMap():
    uri = "layer='2' url='https://sampleserver6.arcgisonline.com/arcgis/rest/services/USA/MapServer'"
    layer = QgsRasterLayer(uri, 'testlayer', 'arcgismapserver')
    assert layer.isValid()

def _loadArcFeature():
    uri = "url='https://sampleserver6.arcgisonline.com/arcgis/rest/services/USA/MapServer/2'"
    layer = QgsVectorLayer(uri, 'testlayer', 'arcgisfeatureserver')
    assert layer.isValid()
    
def _loadWcs():
    valid = {}
    ports = os.getenv(TEST_PORTS).split(",") 
    for port in ports:
        try:
            url = _addPort(os.getenv(TEST_URL) + "/wcs", port)
            uri = QgsDataSourceUri()
            uri.setParam('url',url )
            uri.setParam("identifier", "testlayer")
            layer = QgsRasterLayer(str(uri.encodedUri()), 'testlayer', 'wcs')
            valid[url] = layer.isValid()
        except:
            valid[url] = False
    failed = [k for k,v in valid.items() if not v]
    if failed:
        raise AssertionError("Test failed for the following URLs: " + str(failed))

def _modifyAndLoadWfs():
    valid = {}
    ports = os.getenv(TEST_PORTS).split(",")
    for port in ports:
        try:
            url = _addPort(os.getenv(TEST_URL) + "/wfs", port)
            uri = "%s?typename=union&version=1.0.0&request=GetFeature&service=WFS" % url
            layer = QgsVectorLayer(uri, "testlayer", "WFS")
            featureCount = layer.featureCount()
            featureid = list(layer.getFeatures())[0].id()
            layer.startEditing()    
            layer.deleteFeature(featureid)
            layer.commitChanges()
            layer = QgsVectorLayer(uri, "testlayer", "WFS")
            valid[url] =  layer.featureCount() == featureCount - 1
        except:
            valid[url] = False
    failed = [k for k,v in valid.items() if not v]
    if failed:
        raise AssertionError("Test failed for the following URLs: " + str(failed))

AUTHDB_MASTERPWD = "password"

def _initAuthManager():
    authm = QgsAuthManager.instance()
    # check if QgsAuthManager has been already initialised... a side effect
    # of the QgsAuthManager.init() is that AuthDbPath is set
    if authm.masterPasswordIsSet():
        msg = 'Auth master password not set from passed string'
        assert authm.masterPasswordSame(AUTHDB_MASTERPWD), msg
    else:
        msg = 'Master password could not be set'
        assert authm.setMasterPassword(AUTHDB_MASTERPWD, True), msg


def _populatePKITestCerts():
    removePKITestCerts()
    assert (AUTHCFGID is None)
    # set alice PKI data
    pkipath = os.path.join(os.path.dirname(__file__), 'data', 'certs', 'certs-keys')
    p_config = QgsAuthMethodConfig()
    p_config.setName("alice")
    p_config.setMethod('PKI-PKCS#12')
    p_config.setUri("http://example.com")
    p_config.setConfig("certpath", pkipath 'alice.p12'))
    assert p_config.isValid()
    # add authorities
    cacerts = QSslCertificate.fromPath(os.path.join(pkipath, 'subissuer-issuer-root-ca_issuer-2-root-2-ca_chains.pem'))
    assert cacerts is not None
    authm.storeCertAuthorities(cacerts)
    authm.rebuildCaCertsCache()
    authm.rebuildTrustedCaCertsCache()

    # register alice data in auth
    authm.storeAuthenticationConfig(p_config)
    authid = p_config.id()
    assert (authid is not None)
    assert (authid != '')
    return authid

def _addToDbAndLoadLayer():    
    host = "postgis.boundless.test"
    db = "opengeo"
    username: "docker"
    password = "docker"
    port  = "55432"
    layer = _loadTestLayer()

    #No-PKI
    uri = QgsDataSourceURI()
    uri.setConnection(host, port, db, username, password)
    uri.setDataSource("public", "test", "geom", "", "gid")
    error = QgsVectorLayerExporter.exportLayer(layer, uri, "postgres", None, False, False)
    assert error == QgsVectorLayerExporter.NoError

    uri = QgsDataSourceURI()
    uri.setConnection(host, port, db, username, password)
    uri.setDataSource("", "test", "geom", "", "gid")
    layer = QgsVectorLayer(uri.uri(), "testlayer", "postgres")
    assert layers.isValid()

    #PKI
    _initAuthManager()
    authid = _populatePKITestCerts()

    uri = QgsDataSourceURI()
    uri.setConnection(host, port, db, username, password, QgsDataSourceUri.SslRequire, authid)
    uri.setDataSource("public", "test", "geom", "", "gid")
    error = QgsVectorLayerExporter.exportLayer(layer, uri, "postgres", None, False, False)
    assert error == QgsVectorLayerExporter.NoError

    uri = QgsDataSourceURI()
    uri.setConnection(host, port, db, username, password, QgsDataSourceUri.SslRequire, authid))
    uri.setDataSource("", "test", "geom", "", "gid")
    layer = QgsVectorLayer(uri.uri(), "testlayer", "postgres")
    assert layers.isValid()

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

    arcmapTest = Test("Test ArcMapserver")
    arcmapTest.addStep("Load layer",
                           prestep=_loadArcMap)

    arcfeatureTest = Test("Test ArcFeatureserver")
    arcfeatureTest.addStep("Load layer",
                           prestep=_loadArcFeature)

    wcsTest = Test("Test WCS")
    wcsTest.addStep("Load WCS layer",
                           prestep=_loadWcs)

    wfsTest = Test("Test WFS")
    wfsTest.addStep("Modify and load WFS layer",
                           prestep=_modifyAndLoadWfs)

    return [spatialiteTest, logTest, aboutTest, wcsTest, wfsTest, arcmapTest, arcfeatureTest]

def settings():
    return  {TEST_URL: " https://suite.boundless.test/geoserver/web/",
            TEST_PORTS: "8080,8443"}

def unitTests():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(PackageTests))
    suite.addTests(unittest.makeSuite(TestImports))
    suite.addTests(unittest.makeSuite(TestSupportedFormats))
    suite.addTests(unittest.makeSuite(TestOtherCommandLineUtilities))
    return suite


def run_all():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(unitTests())
