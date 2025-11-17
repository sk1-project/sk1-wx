# -*- coding: utf-8 -*-
"""
Smoke Test 04: UC2 API Initialization

Tests the UC2 (UniConvertor) API initialization and basic functionality.
This tests the programmatic API, not the CLI.

Compatible with Python 2.7 and Python 3.x.
"""

from __future__ import print_function, absolute_import

import pytest


def test_uc2_init():
    """Test initializing UC2 application."""
    from uc2 import uc2_init

    app = uc2_init()
    assert app is not None
    print("UC2 application initialized: {}".format(type(app).__name__))


def test_uc2_app_has_appdata(uc2_app):
    """Test that UC2 app has appdata attribute."""
    assert hasattr(uc2_app, 'appdata')
    assert uc2_app.appdata is not None
    print("AppData type: {}".format(type(uc2_app.appdata).__name__))


def test_uc2_appdata_attributes(uc2_app):
    """Test that appdata has expected attributes."""
    appdata = uc2_app.appdata

    # Should have app_name or similar
    assert hasattr(appdata, 'app_name') or hasattr(appdata, 'name')

    # Should have version or build info
    assert (hasattr(appdata, 'version') or
            hasattr(appdata, 'app_version') or
            hasattr(appdata, 'build'))

    print("AppData attributes: {}".format(dir(appdata)))


def test_uc2_app_config(uc2_app):
    """Test that UC2 app has configuration."""
    # The app should have some config mechanism
    assert hasattr(uc2_app, 'appdata')

    # AppData typically has config
    if hasattr(uc2_app.appdata, 'app_config'):
        assert uc2_app.appdata.app_config is not None
        print("App config available")


def test_get_loader_function():
    """Test the get_loader function from formats module."""
    from uc2.formats import get_loader

    assert callable(get_loader)
    print("get_loader function is callable")


def test_get_saver_function():
    """Test the get_saver function from formats module."""
    from uc2.formats import get_saver

    assert callable(get_saver)
    print("get_saver function is callable")


def test_get_loader_by_id():
    """Test get_loader_by_id with known format."""
    from uc2.formats import get_loader_by_id
    from uc2 import uc2const

    # Try to get SK2 loader
    loader = get_loader_by_id(uc2const.SK2)
    assert loader is not None
    assert callable(loader)
    print("SK2 loader: {}".format(loader))


def test_get_saver_by_id():
    """Test get_saver_by_id with known format."""
    from uc2.formats import get_saver_by_id
    from uc2 import uc2const

    # Try to get SK2 saver
    saver = get_saver_by_id(uc2const.SK2)
    assert saver is not None
    assert callable(saver)
    print("SK2 saver: {}".format(saver))


def test_format_detection_sk2():
    """Test format detection for .sk2 files."""
    from uc2.formats import get_loader

    # Create a fake path (doesn't need to exist for format detection)
    fake_path = '/tmp/test.sk2'
    loader = get_loader(fake_path, return_id=True)

    # Should return (loader_function, format_id) tuple
    assert loader is not None
    if isinstance(loader, tuple):
        loader_func, format_id = loader
        assert callable(loader_func)
        print("SK2 format detected, ID: {}".format(format_id))
    else:
        assert callable(loader)
        print("SK2 loader retrieved")


def test_format_detection_svg():
    """Test format detection for .svg files."""
    from uc2.formats import get_loader

    fake_path = '/tmp/test.svg'
    loader = get_loader(fake_path)

    assert loader is not None
    assert callable(loader)
    print("SVG loader retrieved")


def test_format_detection_pdf():
    """Test format detection for .pdf files."""
    from uc2.formats import get_loader

    fake_path = '/tmp/test.pdf'
    loader = get_loader(fake_path)

    assert loader is not None
    assert callable(loader)
    print("PDF loader retrieved")


def test_sk2_presenter_import():
    """Test importing SK2_Presenter class."""
    from uc2.formats.sk2.sk2_presenter import SK2_Presenter

    assert SK2_Presenter is not None
    print("SK2_Presenter class: {}".format(SK2_Presenter))


def test_create_sk2_presenter(uc2_app):
    """Test creating an SK2_Presenter instance (empty document)."""
    from uc2.formats.sk2.sk2_presenter import SK2_Presenter

    doc = SK2_Presenter(uc2_app.appdata)
    assert doc is not None
    print("Created SK2_Presenter: {}".format(type(doc).__name__))

    # Should have model
    assert hasattr(doc, 'model')
    assert doc.model is not None
    print("Document has model: {}".format(type(doc.model).__name__))

    # Clean up
    doc.close()


def test_sk2_presenter_methods(uc2_app):
    """Test that SK2_Presenter has expected methods."""
    from uc2.formats.sk2.sk2_presenter import SK2_Presenter

    doc = SK2_Presenter(uc2_app.appdata)

    # Should have methods attribute
    assert hasattr(doc, 'methods')
    methods = doc.methods

    # Check for common methods
    assert hasattr(methods, 'get_page')
    assert hasattr(methods, 'get_pages')

    print("SK2_Presenter methods available: {}".format(
        [m for m in dir(methods) if not m.startswith('_')][:10]
    ))

    doc.close()


def test_sk2_get_page(uc2_app):
    """Test getting a page from an SK2 document."""
    from uc2.formats.sk2.sk2_presenter import SK2_Presenter

    doc = SK2_Presenter(uc2_app.appdata)

    # Get the first page
    page = doc.methods.get_page()
    assert page is not None
    print("Got page: {}".format(type(page).__name__))

    doc.close()


def test_format_constants():
    """Test that format constants are defined."""
    from uc2 import uc2const

    # Vector formats
    assert hasattr(uc2const, 'SK2')
    assert hasattr(uc2const, 'SK1')
    assert hasattr(uc2const, 'SVG')
    assert hasattr(uc2const, 'PDF')
    assert hasattr(uc2const, 'CDR')
    assert hasattr(uc2const, 'CMX')

    # Bitmap formats
    assert hasattr(uc2const, 'PNG')
    assert hasattr(uc2const, 'JPEG')

    print("Format constants defined: SK2={}, SVG={}, PDF={}".format(
        uc2const.SK2, uc2const.SVG, uc2const.PDF
    ))


def test_color_space_constants():
    """Test that color space constants are defined."""
    from uc2 import uc2const

    assert hasattr(uc2const, 'COLOR_RGB')
    assert hasattr(uc2const, 'COLOR_CMYK')
    assert hasattr(uc2const, 'COLOR_GRAY')

    print("Color space constants: RGB={}, CMYK={}, GRAY={}".format(
        uc2const.COLOR_RGB, uc2const.COLOR_CMYK, uc2const.COLOR_GRAY
    ))


def test_unit_constants():
    """Test that unit constants are defined."""
    from uc2 import uc2const

    assert hasattr(uc2const, 'UNIT_MM')
    assert hasattr(uc2const, 'UNIT_PT')
    assert hasattr(uc2const, 'UNIT_IN')

    print("Unit constants: MM={}, PT={}, IN={}".format(
        uc2const.UNIT_MM, uc2const.UNIT_PT, uc2const.UNIT_IN
    ))


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
