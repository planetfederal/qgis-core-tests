'''
Tests to ensure that a QGIS installation contains Processing dependencies
and they are correctly configured by default
'''
from builtins import str
import os
import time
import tempfile
import unittest

from qgis.utils import active_plugins
from qgis.core import QgsVectorLayer, QgsVectorFileWriter

from processing.algs.saga.SagaUtils import SAGA_FOLDER, getSagaInstalledVersion
from processing.core.ProcessingConfig import ProcessingConfig
from processing.algs.grass7.Grass7Utils import Grass7Utils
from processing.algs.otb.OTBUtils import findOtbPath


class PackageTests(unittest.TestCase):

    def testSaga(self):
        '''Test SAGA is installed. QGIS-89 (1)'''
        folder = ProcessingConfig.getSetting(SAGA_FOLDER)
        hasSetting = True
        try:
            ProcessingConfig.removeSetting(SAGA_FOLDER)
        except:
            hasSetting = False
        self.assertTrue(getSagaInstalledVersion(True) in ["2.1.2", "2.1.3", "2.1.4", "2.2.0", "2.2.2"])
        if hasSetting:
            ProcessingConfig.setSettingValue(SAGA_FOLDER, folder)


    def testGrass(self):
        '''Test GRASS is installed QGIS-89 (2)'''
        folder = ProcessingConfig.getSetting(Grass7Utils.GRASS_FOLDER)
        ProcessingConfig.removeSetting(Grass7Utils.GRASS_FOLDER)
        msg = Grass7Utils.checkGrass7IsInstalled()
        self.assertIsNone(msg)
        ProcessingConfig.setSettingValue(Grass7Utils.GRASS_FOLDER, folder)


    def testOtb(self):
        '''Test OTB is installed QGIS-89 (3)'''
        folder = findOtbPath()
        self.assertIsNotNone(folder)


    def testCorePluginsAreLoaded(self):
        '''Test core plugins are loaded. QGIS-55'''
        corePlugins = ['processing', 'GdalTools', 'MetaSearch', 'db_manager']
        for p in corePlugins:
            self.assertTrue(p in active_plugins)


    def testGDB(self):
        '''Test GDB format. QGIS-62'''
        layernames = ['T_1_DirtyAreas', 'T_1_PointErrors', 'landbnds', 'counties', 'neighcountry',
                      'cities', 'usabln', 'T_1_LineErrors', 'states', 'T_1_PolyErrors', 'us_lakes',
                      'us_rivers', 'intrstat']
        for layername in layernames:
            layer = QgsVectorLayer(os.path.join(os.path.dirname(__file__), "data",
                                    "ESRI_FileGDB-API_sample_Topo.gdb|layername=%s" % layername),
                                    "test", "ogr")
            self.assertTrue(layer.isValid())


    def testGeoPackage(self):
        '''Test GeoPackage'''
        layer = QgsVectorLayer(os.path.join(os.path.dirname(__file__), "data","airports.gpkg"),
                                    "test", "ogr")
        self.assertTrue(layer.isValid())
        filepath = os.path.join(tempfile.mkdtemp(), str(time.time()) + ".gpkg")
        QgsVectorFileWriter.writeAsVectorFormat(layer, filepath, 'utf-8', layer.crs(), 'GPKG')
        layer = QgsVectorLayer(filepath, "test", "ogr")
        self.assertTrue(layer.isValid())


if __name__ == '__main__':
    unittest.main()
