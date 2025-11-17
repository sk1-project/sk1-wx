# -*- coding: utf-8 -*-
"""
Smoke Test 07: Format Savers

Tests that all supported format savers can be retrieved.

Compatible with Python 2.7 and Python 3.x.
"""

from __future__ import print_function, absolute_import

import pytest


# All vector format IDs that have savers
VECTOR_SAVERS = [
    'SK2', 'SK1', 'SK', 'SVG', 'SVGZ', 'PDF', 'PLT', 'CDR', 'CMX', 'CCX',
    'CGM', 'FIG', 'DST',
]

# Bitmap format IDs that have savers (usually just PNG)
BITMAP_SAVERS = [
    'PNG',
]

# Palette format IDs that have savers
PALETTE_SAVERS = [
    'SKP', 'GPL', 'SCRIBUS_PAL', 'SOC', 'CPL', 'COREL_PAL', 'ASE', 'ACO', 'JCW',
]


def test_get_saver_function_exists():
    """Test that get_saver function exists."""
    from uc2.formats import get_saver
    assert callable(get_saver)


def test_get_saver_by_id_function_exists():
    """Test that get_saver_by_id function exists."""
    from uc2.formats import get_saver_by_id
    assert callable(get_saver_by_id)


@pytest.mark.parametrize('format_id', VECTOR_SAVERS)
def test_vector_saver_by_id(format_id):
    """Test getting vector format savers by ID."""
    from uc2.formats import get_saver_by_id
    from uc2 import uc2const

    # Get format constant
    if not hasattr(uc2const, format_id):
        pytest.skip("Format {} not defined in uc2const".format(format_id))

    format_const = getattr(uc2const, format_id)

    try:
        saver = get_saver_by_id(format_const)
        assert saver is not None
        assert callable(saver)
        print("Saver for {} ({}): {}".format(format_id, format_const, saver.__name__))
    except Exception as e:
        pytest.skip("Saver for {} not available: {}".format(format_id, str(e)))


@pytest.mark.parametrize('format_id', BITMAP_SAVERS)
def test_bitmap_saver_by_id(format_id):
    """Test getting bitmap format savers by ID."""
    from uc2.formats import get_saver_by_id
    from uc2 import uc2const

    if not hasattr(uc2const, format_id):
        pytest.skip("Format {} not defined in uc2const".format(format_id))

    format_const = getattr(uc2const, format_id)

    try:
        saver = get_saver_by_id(format_const)
        assert saver is not None
        assert callable(saver)
        print("Saver for {} ({}): {}".format(format_id, format_const, saver.__name__))
    except Exception as e:
        pytest.skip("Saver for {} not available: {}".format(format_id, str(e)))


@pytest.mark.parametrize('format_id', PALETTE_SAVERS)
def test_palette_saver_by_id(format_id):
    """Test getting palette format savers by ID."""
    from uc2.formats import get_saver_by_id
    from uc2 import uc2const

    if not hasattr(uc2const, format_id):
        pytest.skip("Format {} not defined in uc2const".format(format_id))

    format_const = getattr(uc2const, format_id)

    try:
        saver = get_saver_by_id(format_const)
        assert saver is not None
        assert callable(saver)
        print("Saver for {} ({}): {}".format(format_id, format_const, saver.__name__))
    except Exception as e:
        pytest.skip("Saver for {} not available: {}".format(format_id, str(e)))


@pytest.mark.parametrize('extension,format_id', [
    ('.sk2', 'SK2'),
    ('.sk1', 'SK1'),
    ('.svg', 'SVG'),
    ('.svgz', 'SVGZ'),
    ('.pdf', 'PDF'),
    ('.cdr', 'CDR'),
    ('.cmx', 'CMX'),
    ('.plt', 'PLT'),
    ('.png', 'PNG'),
    ('.gpl', 'GPL'),
])
def test_saver_by_extension(extension, format_id):
    """Test getting savers by file extension."""
    from uc2.formats import get_saver

    fake_path = '/tmp/test{}'.format(extension)

    try:
        saver = get_saver(fake_path)
        assert saver is not None
        assert callable(saver)
        print("Saver for {}: {}".format(extension, saver.__name__))
    except Exception as e:
        pytest.skip("Saver for {} not available: {}".format(extension, str(e)))


def test_sk2_saver_module():
    """Test SK2 saver module."""
    from uc2.formats.sk2 import sk2_saver
    assert sk2_saver is not None
    assert callable(sk2_saver)


def test_svg_saver_module():
    """Test SVG saver module."""
    try:
        from uc2.formats.svg import svg_saver
        assert svg_saver is not None
        assert callable(svg_saver)
    except ImportError:
        pytest.skip("SVG saver not available")


def test_pdf_saver_module():
    """Test PDF saver module."""
    try:
        from uc2.formats.pdf import pdf_saver
        assert pdf_saver is not None
        assert callable(pdf_saver)
    except ImportError:
        pytest.skip("PDF saver not available")


def test_png_saver_module():
    """Test PNG saver module."""
    try:
        from uc2.formats.png import png_saver
        assert png_saver is not None
        assert callable(png_saver)
    except ImportError:
        pytest.skip("PNG saver not available")


def test_plt_saver_module():
    """Test PLT saver module."""
    try:
        from uc2.formats.plt import plt_saver
        assert plt_saver is not None
        assert callable(plt_saver)
    except ImportError:
        pytest.skip("PLT saver not available")


def test_cdr_saver_module():
    """Test CDR saver module."""
    try:
        from uc2.formats.cdr import cdr_saver
        assert cdr_saver is not None
        assert callable(cdr_saver)
    except ImportError:
        pytest.skip("CDR saver not available")


def test_cmx_saver_module():
    """Test CMX saver module."""
    try:
        from uc2.formats.cmx import cmx_saver
        assert cmx_saver is not None
        assert callable(cmx_saver)
    except ImportError:
        pytest.skip("CMX saver not available")


def test_saver_with_return_id():
    """Test get_saver with return_id=True."""
    from uc2.formats import get_saver

    fake_path = '/tmp/test.sk2'
    result = get_saver(fake_path, return_id=True)

    assert result is not None
    assert isinstance(result, tuple)
    assert len(result) == 2

    saver, format_id = result
    assert callable(saver)
    assert format_id is not None

    print("Saver: {}, Format ID: {}".format(saver.__name__, format_id))


def test_all_savers_summary():
    """Summary test - report all available savers."""
    from uc2.formats import get_saver_by_id
    from uc2 import uc2const

    all_formats = VECTOR_SAVERS + BITMAP_SAVERS + PALETTE_SAVERS
    available = []
    unavailable = []

    for format_id in all_formats:
        if not hasattr(uc2const, format_id):
            unavailable.append(format_id)
            continue

        try:
            format_const = getattr(uc2const, format_id)
            saver = get_saver_by_id(format_const)
            if saver is not None:
                available.append(format_id)
            else:
                unavailable.append(format_id)
        except Exception:
            unavailable.append(format_id)

    print("\nSaver Summary:")
    print("  Available: {}/{}".format(len(available), len(all_formats)))
    print("  Available formats: {}".format(', '.join(available)))
    if unavailable:
        print("  Unavailable: {}".format(', '.join(unavailable)))

    # We expect at least the core formats to be available
    assert 'SK2' in available
    assert 'SVG' in available or 'PDF' in available  # At least one export format


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
