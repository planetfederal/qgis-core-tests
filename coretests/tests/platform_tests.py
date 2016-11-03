# -*- coding: utf-8 -*-

"""
***************************************************************************
    Tests for Boundless Desktop command line utilities and python modules.

    Tests that common GIS related python modules are available and that
    selected command line utilities can be invoked from the command line.

    ---------------------
    Date                 : June 2016
    Copyright            : © 2016 Boundless
    Contact              : info@boundlessgeo.com
    Author               : Alessandro Pasotti

***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Alessandro Pasotti'
__date__ = '2016/06/20'
__copyright__ = 'Copyright 2016, Boundless'
# This will get replaced with a git SHA1 when you do a git archive
__revision__ = '$Format:%H$'

import unittest
import subprocess
import platform

# List of command line utilities to be tested
COMMAND_LINE_UTILITIES = [
    'qgis --help',
    'grass70 --help',
    'ogr2ogr --help',
    'gdalinfo --help',
    'ogrinfo --help',
    'cs2cs',
]

GDAL_EXPECTED_FORMATS = [
    #'ECW', # No Mac
    #'JP2ECW', # No Mac
    #'GeoRaster', # No Mac
    #'MG4Lidar', # No Mac
    #'MrSID', # No Mac
    'VRT',
    'GTiff',
    'NITF',
    'RPFTOC',
    'ECRGTOC',
    'HFA',
    'SAR_CEOS',
    'CEOS',
    'JAXAPALSAR',
    'GFF',
    'ELAS',
    'AIG',
    'AAIGrid',
    'GRASSASCIIGrid',
    'SDTS',
    #'OGDI', # No Mac
    'DTED',
    'PNG',
    'JPEG',
    'MEM',
    'JDEM',
    'GIF',
    'BIGGIF',
    'ESAT',
    'BSB',
    'XPM',
    'BMP',
    'DIMAP',
    'AirSAR',
    'RS2',
    'PCIDSK',
    'PCRaster',
    'ILWIS',
    'SGI',
    'SRTMHGT',
    'Leveller',
    'Terragen',
    'GMT',
    'netCDF',
    #'HDF4', # No Mac
    #'HDF4Image', # No Mac
    'ISIS3',
    'ISIS2',
    'PDS',
    'VICAR',
    'TIL',
    'ERS',
    'JP2OpenJPEG',
    'L1B',
    'FIT',
    'GRIB',
    'RMF',
    'WCS',
    'WMS',
    'MSGN',
    'RST',
    'INGR',
    'GSAG',
    'GSBG',
    'GS7BG',
    'COSAR',
    'TSX',
    'COASP',
    'R',
    'MAP',
    'PNM',
    'DOQ1',
    'DOQ2',
    'ENVI',
    'EHdr',
    'GenBin',
    'PAux',
    'MFF',
    'MFF2',
    'FujiBAS',
    'GSC',
    'FAST',
    'BT',
    'LAN',
    'CPG',
    'IDA',
    'NDF',
    'EIR',
    'DIPEx',
    'LCP',
    'GTX',
    'LOSLAS',
    'NTv2',
    'CTable2',
    'ACE2',
    'SNODAS',
    'KRO',
    'ROI_PAC',
    'ARG',
    'RIK',
    'USGSDEM',
    'GXF',
    'BAG',
    'HDF5',
    'HDF5Image',
    'NWT_GRD',
    'NWT_GRC',
    'ADRG',
    'SRP',
    'BLX',
    'Rasterlite',
    'PostGISRaster',
    'SAGA',
    'KMLSUPEROVERLAY',
    'XYZ',
    'HF2',
    'PDF',
    'OZI',
    'CTG',
    'E00GRID',
    'ZMap',
    'NGSGEOID',
    'MBTiles',
    'IRIS',
    'PLMOSAIC',
    'GPKG',
    'PLSCENES',
    'HTTP',
]


OGR_EXPECTED_FORMATS = [
    #'JP2ECW', # No Mac
    #'FileGDB',
    #'OCI',
    #'SOSI',
    'PCIDSK',
    'JP2OpenJPEG',
    'PDF',
    'ESRI',
    'MapInfo',
    'UK',
    'OGR_SDTS',
    'S57',
    'DGN',
    'OGR_VRT',
    'REC',
    'Memory',
    'BNA',
    'CSV',
    'NAS',
    'GML',
    'GPX',
    'LIBKML',
    'KML',
    'GeoJSON',
    'Interlis',
    'Interlis',
    'OGR_GMT',
    'GPKG',
    'SQLite',
    'ODBC',
    'WAsP',
    'PGeo',
    'MSSQLSpatial',
    #'OGR_OGDI',
    'PostgreSQL',
    #'MySQL',
    'OpenFileGDB',
    'XPlane',
    'DXF',
    'Geoconcept',
    'GeoRSS',
    'GPSTrackMaker',
    'VFK',
    'PGDUMP',
    'OSM',
    'GPSBabel',
    'SUA',
    'OpenAir',
    'OGR_PDS',
    'WFS',
    'HTF',
    'AeronavFAA',
    'Geomedia',
    'EDIGEO',
    'GFT',
    #'GME',
    'SVG',
    'CouchDB',
    'Cloudant',
    'Idrisi',
    'ARCGEN',
    'SEGUKOOA',
    'SEGY',
    'XLS',
    'ODS',
    'XLSX',
    'ElasticSearch',
    'Walk',
    'Carto',
    'SXF',
    'Selafin',
    'JML',
    'PLSCENES',
    'CSW',
    'TIGER',
    'AVCBin',
    'AVCE00',
    'HTTP',
]


class TestImports(unittest.TestCase):

    def test_QgisImports(self):
        """Test that core and gui classes can be imported"""
        from qgis import core
        from qgis import gui

    def test_OSGEOImports(self):
        """Test that GDAL/OGR can be imported"""
        from osgeo import gdal
        from osgeo import ogr

    def test_matPlotLibImports(self):
        """Test that matplotlib can be imported"""
        import matplotlib

    def test_numpyImports(self):
        """Test that numpy can be imported"""
        import numpy

    def test_IPythonImports(self):
        """Test that IPython can be imported"""
        import IPython


class TestSupportedFormats(unittest.TestCase):
    """Test that GDAL OGR formats are available"""

    def test_GDALFormats(self):
        """Test that all required formats are enabled"""
        process = subprocess.Popen(['gdalinfo', '--formats'],
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        out, err = process.communicate()
        formats = [f.strip().split(' ')[0] for f in out.split("\n")[1:] if f]
        for f in GDAL_EXPECTED_FORMATS:
            self.assertTrue(f in formats, "GDAL Format %s is not supported!" % f)

    def test_OGRFormats(self):
        """Test that all required formats are enabled"""
        process = subprocess.Popen(['ogrinfo', '--formats'],
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        out, err = process.communicate()
        formats = [f.strip().split(' ')[0] for f in out.split("\n")[1:] if f]
        for f in OGR_EXPECTED_FORMATS:
            self.assertTrue(f in formats,
                            "OGR Format %s is not supported!" % f)


class TestOtherCommandLineUtilities(unittest.TestCase):
    """Test that selected command line utilities are available"""

    def test_commandLineUtilities(self):
        """Test that cmd line utilities can run"""
        system = platform.system()
        for utility in COMMAND_LINE_UTILITIES:
            try:
                command = utility.split(' ')
                subprocess.check_call(command, shell=system == 'Windows',
                                               stdin=subprocess.PIPE,
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE)
            except subprocess.CalledProcessError, e:
                print("Utility %s exited with : %s" % (utility, e.returncode))
            except Exception, e:
                raise AssertionError("Utility %s cannot run: %s" % (utility, e))


if __name__ == '__main__':
    unittest.main()
