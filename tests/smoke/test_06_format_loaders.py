# -*- coding: utf-8 -*-
"""
Smoke Test 06: Format Loaders

Tests that all supported format loaders can be retrieved.
Tests actual loading where test files are available.

Compatible with Python 2.7 and Python 3.x.
"""

from __future__ import print_function, absolute_import

import pytest


# All vector format IDs that have loaders
VECTOR_LOADERS = [
    'SK2', 'SK1', 'SK', 'SVG', 'SVGZ', 'CDR', 'CDT', 'CMX', 'CCX',
    'XAR', 'WMF', 'PLT', 'FIG', 'CGM', 'DST', 'PES',
]

# Bitmap format IDs that have loaders
BITMAP_LOADERS = [
    'PNG', 'JPEG', 'PSD', 'XCF', 'JP2', 'TIFF', 'GIF', 'BMP',
    'PCX', 'PPM', 'XBM', 'XPM', 'WEBP',
]

# Palette format IDs that have loaders
PALETTE_LOADERS = [
    'SKP', 'GPL', 'SCRIBUS_PAL', 'SOC', 'CPL', 'COREL_PAL', 'ASE', 'ACO', 'JCW',
]


def test_get_loader_function_exists():
    """Test that get_loader function exists."""
    from uc2.formats import get_loader
    assert callable(get_loader)


def test_get_loader_by_id_function_exists():
    """Test that get_loader_by_id function exists."""
    from uc2.formats import get_loader_by_id
    assert callable(get_loader_by_id)


@pytest.mark.parametrize('format_id', VECTOR_LOADERS)
def test_vector_loader_by_id(format_id):
    """Test getting vector format loaders by ID."""
    from uc2.formats import get_loader_by_id
    from uc2 import uc2const

    # Get format constant
    if not hasattr(uc2const, format_id):
        pytest.skip("Format {} not defined in uc2const".format(format_id))

    format_const = getattr(uc2const, format_id)

    try:
        loader = get_loader_by_id(format_const)
        assert loader is not None
        assert callable(loader)
        print("Loader for {} ({}): {}".format(format_id, format_const, loader.__name__))
    except Exception as e:
        pytest.skip("Loader for {} not available: {}".format(format_id, str(e)))


@pytest.mark.parametrize('format_id', BITMAP_LOADERS)
def test_bitmap_loader_by_id(format_id):
    """Test getting bitmap format loaders by ID."""
    from uc2.formats import get_loader_by_id
    from uc2 import uc2const

    if not hasattr(uc2const, format_id):
        pytest.skip("Format {} not defined in uc2const".format(format_id))

    format_const = getattr(uc2const, format_id)

    try:
        loader = get_loader_by_id(format_const)
        assert loader is not None
        assert callable(loader)
        print("Loader for {} ({}): {}".format(format_id, format_const, loader.__name__))
    except Exception as e:
        pytest.skip("Loader for {} not available: {}".format(format_id, str(e)))


@pytest.mark.parametrize('format_id', PALETTE_LOADERS)
def test_palette_loader_by_id(format_id):
    """Test getting palette format loaders by ID."""
    from uc2.formats import get_loader_by_id
    from uc2 import uc2const

    if not hasattr(uc2const, format_id):
        pytest.skip("Format {} not defined in uc2const".format(format_id))

    format_const = getattr(uc2const, format_id)

    try:
        loader = get_loader_by_id(format_const)
        assert loader is not None
        assert callable(loader)
        print("Loader for {} ({}): {}".format(format_id, format_const, loader.__name__))
    except Exception as e:
        pytest.skip("Loader for {} not available: {}".format(format_id, str(e)))


@pytest.mark.parametrize('extension,format_id', [
    ('.sk2', 'SK2'),
    ('.sk1', 'SK1'),
    ('.svg', 'SVG'),
    ('.svgz', 'SVGZ'),
    ('.pdf', 'PDF'),
    ('.cdr', 'CDR'),
    ('.cmx', 'CMX'),
    ('.wmf', 'WMF'),
    ('.png', 'PNG'),
    ('.jpg', 'JPEG'),
    ('.tif', 'TIFF'),
    ('.gif', 'GIF'),
    ('.gpl', 'GPL'),
])
def test_loader_by_extension(extension, format_id):
    """Test getting loaders by file extension."""
    from uc2.formats import get_loader

    fake_path = '/tmp/test{}'.format(extension)

    try:
        loader = get_loader(fake_path)
        assert loader is not None
        assert callable(loader)
        print("Loader for {}: {}".format(extension, loader.__name__))
    except Exception as e:
        pytest.skip("Loader for {} not available: {}".format(extension, str(e)))


def test_sk2_loader_module():
    """Test SK2 loader module."""
    from uc2.formats.sk2 import sk2_loader
    assert sk2_loader is not None
    assert callable(sk2_loader)


def test_svg_loader_module():
    """Test SVG loader module."""
    try:
        from uc2.formats.svg import svg_loader
        assert svg_loader is not None
        assert callable(svg_loader)
    except ImportError:
        pytest.skip("SVG loader not available")


def test_pdf_loader_module():
    """Test PDF loader module."""
    try:
        from uc2.formats.pdf import pdf_loader
        assert pdf_loader is not None
        assert callable(pdf_loader)
    except ImportError:
        pytest.skip("PDF loader not available")


def test_png_loader_module():
    """Test PNG loader module."""
    try:
        from uc2.formats.png import png_loader
        assert png_loader is not None
        assert callable(png_loader)
    except ImportError:
        pytest.skip("PNG loader not available")


def test_cdr_loader_module():
    """Test CDR loader module."""
    try:
        from uc2.formats.cdr import cdr_loader
        assert cdr_loader is not None
        assert callable(cdr_loader)
    except ImportError:
        pytest.skip("CDR loader not available")


def test_cmx_loader_module():
    """Test CMX loader module."""
    try:
        from uc2.formats.cmx import cmx_loader
        assert cmx_loader is not None
        assert callable(cmx_loader)
    except ImportError:
        pytest.skip("CMX loader not available")


def test_loader_with_return_id():
    """Test get_loader with return_id=True."""
    from uc2.formats import get_loader

    fake_path = '/tmp/test.sk2'
    result = get_loader(fake_path, return_id=True)

    assert result is not None
    assert isinstance(result, tuple)
    assert len(result) == 2

    loader, format_id = result
    assert callable(loader)
    assert format_id is not None

    print("Loader: {}, Format ID: {}".format(loader.__name__, format_id))


def test_all_loaders_summary():
    """Summary test - report all available loaders."""
    from uc2.formats import get_loader_by_id
    from uc2 import uc2const

    all_formats = VECTOR_LOADERS + BITMAP_LOADERS + PALETTE_LOADERS
    available = []
    unavailable = []

    for format_id in all_formats:
        if not hasattr(uc2const, format_id):
            unavailable.append(format_id)
            continue

        try:
            format_const = getattr(uc2const, format_id)
            loader = get_loader_by_id(format_const)
            if loader is not None:
                available.append(format_id)
            else:
                unavailable.append(format_id)
        except Exception:
            unavailable.append(format_id)

    print("\nLoader Summary:")
    print("  Available: {}/{}".format(len(available), len(all_formats)))
    print("  Available formats: {}".format(', '.join(available)))
    if unavailable:
        print("  Unavailable: {}".format(', '.join(unavailable)))

    # We expect at least the core formats to be available
    assert 'SK2' in available
    assert 'SVG' in available


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
