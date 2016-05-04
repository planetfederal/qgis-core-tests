# Tests for the QGIS Tester plugin. To know more see
# https://github.com/boundlessgeo/qgis-tester-plugin

from qgis.utils import *
from qgis.core import *

def functionalTests():
    try:
        from qgistester.test import Test
        from qgistester.utils import loadLayer
    except:
        return []

    test = Test("Empty test")
    test.addStep("Empty step")
    return [test]


def unitTests():
    _tests = []
    #add unit tests with _tests.extend(test_suite)    
    return _tests