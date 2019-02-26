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
from qgis.core import QgsVectorLayer, QgsVectorFileWriter, QgsProject, QgsRasterLayer, QgsProcessingContext, QgsApplication, QgsProcessingFeedback

from processing.algs.saga.SagaUtils import getInstalledVersion, findSagaFolder
from processing.core.ProcessingConfig import ProcessingConfig
from processing.algs.grass7.Grass7Utils import Grass7Utils


class PackageTests(unittest.TestCase):

    def testSaga(self):
        '''Test SAGA is installed. QGIS-89 (1)'''
        self.assertTrue(getInstalledVersion(True).startswith('2.3.'))

    def testGrass(self):
        '''Test GRASS is installed QGIS-89 (2)'''
        folder = ProcessingConfig.getSetting(Grass7Utils.GRASS_FOLDER)
        try:
            ProcessingConfig.removeSetting(Grass7Utils.GRASS_FOLDER)
        except KeyError:
            pass
        msg = Grass7Utils.checkGrassIsInstalled()
        self.assertIsNone(msg)
        ProcessingConfig.setSettingValue(Grass7Utils.GRASS_FOLDER, folder)

    def testCorePluginsAreLoaded(self):
        '''Test core plugins are loaded. QGIS-55'''
        corePlugins = ['processing', 'MetaSearch', 'db_manager']
        for p in corePlugins:
            self.assertTrue(p in active_plugins, "Plugin '%s' not in %s" % (p, str(active_plugins)))            

    def testGDB(self):
        '''Test GDB format. QGIS-62'''
        layernames = ['T_1_DirtyAreas', 'T_1_PointErrors', 'landbnds', 'counties', 'neighcountry',
                      'cities', 'usabln', 'T_1_LineErrors', 'states', 'T_1_PolyErrors', 'us_lakes',
                      'us_rivers', 'intrstat']
        for layername in layernames:
            layer = QgsVectorLayer(os.path.join(os.path.dirname(__file__), "data",
                                    "ESRI_FileGDB-API_sample_Topo.gdb|layername=%s" % layername),
                                    "test", "ogr")
            self.assertTrue(layer.isValid(), "layer '%s' is not valid" % layername)


    def testGeoPackage(self):
        '''Test GeoPackage'''
        layer = QgsVectorLayer(os.path.join(os.path.dirname(__file__), "data","airports.gpkg"),
                                    "test", "ogr")

        self.assertTrue(layer.isValid())
        filepath = os.path.join(tempfile.mkdtemp(), str(time.time()) + ".gpkg")
        QgsVectorFileWriter.writeAsVectorFormat(layer, filepath, 'utf-8', layer.crs(), 'GPKG')
        layer = QgsVectorLayer(filepath, "test", "ogr")
        self.assertTrue(layer.isValid())


    def testGdalScripts(self):
        '''Test GDAL scripts2'''
        layer = QgsRasterLayer(os.path.join(os.path.dirname(__file__), "data","dem25.tif"),
                                    "dem")
        QgsProject.instance().addMapLayer(layer)
        context = QgsProcessingContext()
        context.setProject(QgsProject.instance())

        alg = QgsApplication.processingRegistry().createAlgorithmById('gdal:rastercalculator')
        self.assertIsNotNone(alg)

        parameters = {'INPUT_A':'dem',
                        'BAND_A':1,'INPUT_B':None,'BAND_B':-1,
                        'INPUT_C':None,'BAND_C':-1,'INPUT_D':None,
                        'BAND_D':-1,'INPUT_E':None,'BAND_E':-1,
                        'INPUT_F':None,'BAND_F':-1,'FORMULA':'A*2',
                        'NO_DATA':None,'RTYPE':5,'OPTIONS':'',
                        'OUTPUT':'TEMPORARY_OUTPUT'}
        feedback = QgsProcessingFeedback()

        results, ok = alg.run(parameters, context, feedback)
        self.assertTrue(ok)
        self.assertTrue(os.path.exists(results["OUTPUT"]))

        QgsProject.instance().removeMapLayer(layer)        


if __name__ == '__main__':
    unittest.main()
