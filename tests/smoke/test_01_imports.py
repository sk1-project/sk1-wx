# -*- coding: utf-8 -*-
"""
Smoke Test 01: Core Module Imports

Tests that all core Python modules can be imported without errors.
This is the first sanity check - if modules don't import, nothing else will work.

Compatible with Python 2.7 and Python 3.x.
"""

from __future__ import print_function, absolute_import

import sys
import pytest


def test_python_version():
    """Verify Python version is either 2.7 or 3.x."""
    version = sys.version_info
    assert version[0] in (2, 3), "Python version must be 2.x or 3.x"

    if version[0] == 2:
        assert version[1] >= 7, "Python 2.7+ required"
        print("Running on Python {}.{}.{}".format(version[0], version[1], version[2]))
    else:
        print("Running on Python {}.{}.{}".format(version[0], version[1], version[2]))


def test_import_uc2():
    """Test importing the UC2 (UniConvertor) package."""
    import uc2
    assert uc2 is not None
    assert hasattr(uc2, 'uc2_init')


def test_import_uc2_submodules():
    """Test importing UC2 submodules."""
    # Core modules
    from uc2 import uc2const
    from uc2 import cms
    from uc2 import libcairo
    from uc2 import libgeom
    from uc2 import libpango
    from uc2 import utils

    assert uc2const is not None
    assert cms is not None
    assert libcairo is not None
    assert libgeom is not None
    assert libpango is not None
    assert utils is not None


def test_import_uc2_formats():
    """Test importing UC2 formats module."""
    from uc2 import formats
    assert formats is not None
    assert hasattr(formats, 'get_loader')
    assert hasattr(formats, 'get_saver')
    assert hasattr(formats, 'get_loader_by_id')
    assert hasattr(formats, 'get_saver_by_id')


def test_import_uc2_format_handlers():
    """Test importing specific format handler modules."""
    # SK2 format (native)
    from uc2.formats import sk2
    assert sk2 is not None

    # Common formats
    from uc2.formats import svg
    from uc2.formats import pdf
    from uc2.formats import png

    assert svg is not None
    assert pdf is not None
    assert png is not None


def test_import_sk1():
    """Test importing the SK1 GUI application package."""
    import sk1
    assert sk1 is not None
    assert hasattr(sk1, 'sk1_run')


def test_import_sk1_submodules():
    """Test importing SK1 submodules (non-GUI parts)."""
    from sk1 import app_conf
    from sk1 import app_cms

    assert app_conf is not None
    assert app_cms is not None


def test_import_sk1_document():
    """Test importing SK1 document modules."""
    from sk1.document import presenter
    from sk1.document import api

    assert presenter is not None
    assert api is not None


def test_import_wal():
    """Test importing WAL (Widget Abstraction Layer)."""
    # WAL wraps wxPython, so this might fail if wxPython is not installed
    # or if DISPLAY is not available
    try:
        import wal
        assert wal is not None
        print("WAL imported successfully")
    except ImportError as e:
        pytest.skip("WAL not available: {}".format(str(e)))


def test_import_uc2_constants():
    """Test importing and checking UC2 constants."""
    from uc2 import uc2const

    # Check format ID constants exist
    assert hasattr(uc2const, 'SK2')
    assert hasattr(uc2const, 'SVG')
    assert hasattr(uc2const, 'PDF')
    assert hasattr(uc2const, 'PNG')

    # Check color space constants
    assert hasattr(uc2const, 'COLOR_RGB')
    assert hasattr(uc2const, 'COLOR_CMYK')
    assert hasattr(uc2const, 'COLOR_GRAY')

    # Check unit constants
    assert hasattr(uc2const, 'UNIT_MM')
    assert hasattr(uc2const, 'UNIT_PT')
    assert hasattr(uc2const, 'UNIT_IN')


def test_uc2_version():
    """Test that UC2 has version information."""
    import uc2
    # UC2 should have some version-related attributes
    assert hasattr(uc2, '__version__') or hasattr(uc2, 'VERSION')


def test_import_translation_modules():
    """Test importing translation/locale modules."""
    try:
        from uc2 import msgconst
        assert msgconst is not None
    except ImportError:
        # msgconst might not exist in all versions
        pass


def test_import_sk2_presenter():
    """Test importing SK2 presenter (document model)."""
    from uc2.formats.sk2.sk2_presenter import SK2_Presenter
    assert SK2_Presenter is not None


def test_import_sk2_model():
    """Test importing SK2 model classes."""
    from uc2.formats.sk2 import sk2_model
    assert sk2_model is not None
    assert hasattr(sk2_model, 'SK2_Document')


def test_import_cms_module():
    """Test importing CMS (Color Management System) module."""
    from uc2 import cms
    assert cms is not None
    # Should have libcms (native extension) or pure Python fallback
    assert hasattr(cms, 'libcms') or hasattr(cms, 'ColorManager')


if __name__ == '__main__':
    # Allow running this test file directly
    pytest.main([__file__, '-v'])
