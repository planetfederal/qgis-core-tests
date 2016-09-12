# qgis-core-tests

Tests for the QGIS tester plugin, not related to any Boundless plugin

This repository also hosts other Python tests that are not meant to be run
from the tester plugin inside QGIS, like the tests for the command
line utilities and Python modules.

# Tests list for the Tester plugin:

## Manual and semi-automated tests

- Test Spatialite. QGIS-72
- Verify dependency versions and providers in About dialog. QGIS-53
- Verify in-app message log has no errors for default install. QGIS-54

## Fully automated tests

- Test core plugins are loaded. QGIS-55'
- Test GDB format. QGIS-62
- Test GeoPackage
- Test SAGA is installed. QGIS-89
- Test GRASS is installed QGIS-89
- Test OTB is installed QGIS-89
- Test that core and gui classes can be imported
- Test that GDAL/OGR can be imported
- Test that matplotlib can be imported
- Test that numpy can be imported
- Test that all required formats are enabled
- Test that cmd line utilities can run