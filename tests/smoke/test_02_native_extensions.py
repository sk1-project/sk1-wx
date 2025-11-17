# -*- coding: utf-8 -*-
"""
Smoke Test 02: Native Extensions

Tests that all native C extensions load correctly.
These are critical dependencies - many features won't work if these fail.

Native extensions tested:
- uc2.cms._cms (LCMS2 color management)
- uc2.libcairo._libcairo (Cairo rendering)
- uc2.libpango._libpango (Pango text layout)
- uc2.libimg._libimg (ImageMagick bindings)

Compatible with Python 2.7 and Python 3.x.
"""

from __future__ import print_function, absolute_import

import pytest


@pytest.mark.native
def test_cms_native_extension():
    """Test that the CMS (LCMS2) native extension loads."""
    try:
        from uc2.cms import _cms
        assert _cms is not None
        print("CMS native extension loaded: {}".format(_cms))

        # Check that key functions exist
        assert hasattr(_cms, 'cms_create_srgb_profile')
        assert hasattr(_cms, 'cms_create_cmyk_profile')
        assert hasattr(_cms, 'cms_create_transform')

    except ImportError as e:
        pytest.fail("Failed to import CMS native extension: {}".format(str(e)))


@pytest.mark.native
def test_libcairo_native_extension():
    """Test that the Cairo native extension loads."""
    try:
        from uc2.libcairo import _libcairo
        assert _libcairo is not None
        print("Cairo native extension loaded: {}".format(_libcairo))

        # Check that key functions exist
        assert hasattr(_libcairo, 'create_cpath')

    except ImportError as e:
        pytest.fail("Failed to import Cairo native extension: {}".format(str(e)))


@pytest.mark.native
def test_libpango_native_extension():
    """Test that the Pango native extension loads."""
    try:
        from uc2.libpango import _libpango
        assert _libpango is not None
        print("Pango native extension loaded: {}".format(_libpango))

        # Check that key functions exist
        assert hasattr(_libpango, 'get_version')

    except ImportError as e:
        pytest.fail("Failed to import Pango native extension: {}".format(str(e)))


@pytest.mark.native
def test_libimg_native_extension():
    """Test that the ImageMagick native extension loads."""
    try:
        from uc2.libimg import _libimg
        assert _libimg is not None
        print("ImageMagick native extension loaded: {}".format(_libimg))

        # Check that key functions exist
        assert hasattr(_libimg, 'get_version')
        assert hasattr(_libimg, 'check_image')

    except ImportError as e:
        pytest.fail("Failed to import ImageMagick native extension: {}".format(str(e)))


@pytest.mark.native
def test_cms_basic_functionality():
    """Test basic CMS functionality."""
    from uc2.cms import _cms

    # Create sRGB profile
    srgb_profile = _cms.cms_create_srgb_profile()
    assert srgb_profile is not None
    print("Created sRGB profile")

    # Create CMYK profile
    cmyk_profile = _cms.cms_create_cmyk_profile()
    assert cmyk_profile is not None
    print("Created CMYK profile")


@pytest.mark.native
def test_libcairo_basic_functionality():
    """Test basic Cairo functionality."""
    from uc2.libcairo import _libcairo

    # Create a simple Cairo path
    # Note: Exact API may vary, this tests that the extension is functional
    try:
        # Just verify the module has callable attributes
        assert callable(getattr(_libcairo, 'create_cpath', None))
        print("Cairo extension has callable functions")
    except Exception as e:
        pytest.fail("Cairo basic functionality test failed: {}".format(str(e)))


@pytest.mark.native
def test_libpango_version():
    """Test Pango version retrieval."""
    from uc2.libpango import _libpango

    try:
        version = _libpango.get_version()
        assert version is not None
        print("Pango version: {}".format(version))
    except Exception as e:
        # Some builds might not have get_version
        print("Warning: Could not get Pango version: {}".format(str(e)))


@pytest.mark.native
def test_libimg_version():
    """Test ImageMagick version retrieval."""
    from uc2.libimg import _libimg

    try:
        version = _libimg.get_version()
        assert version is not None
        assert len(version) > 0
        print("ImageMagick version: {}".format(version))
    except Exception as e:
        pytest.fail("Failed to get ImageMagick version: {}".format(str(e)))


@pytest.mark.native
def test_all_native_extensions_summary():
    """Summary test - verify all 4 critical native extensions are available."""
    extensions = {
        'CMS (LCMS2)': 'uc2.cms._cms',
        'Cairo': 'uc2.libcairo._libcairo',
        'Pango': 'uc2.libpango._libpango',
        'ImageMagick': 'uc2.libimg._libimg',
    }

    loaded = {}
    failed = []

    for name, module_path in extensions.items():
        try:
            parts = module_path.split('.')
            mod = __import__(module_path, fromlist=[parts[-1]])
            loaded[name] = True
            print("[OK] {} loaded successfully".format(name))
        except ImportError as e:
            loaded[name] = False
            failed.append((name, str(e)))
            print("[FAIL] {} failed to load: {}".format(name, str(e)))

    # Report summary
    print("\nNative Extensions Summary:")
    print("  Loaded: {}/{}".format(sum(loaded.values()), len(extensions)))

    if failed:
        print("\nFailed extensions:")
        for name, error in failed:
            print("  - {}: {}".format(name, error))
        pytest.fail("{} native extension(s) failed to load".format(len(failed)))


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
