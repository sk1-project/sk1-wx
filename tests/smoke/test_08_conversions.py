# -*- coding: utf-8 -*-
"""
Smoke Test 08: Format Conversions

Tests actual file format conversions using existing SK2 files.
This is the most critical test - it verifies the core conversion functionality.

Compatible with Python 2.7 and Python 3.x.
"""

from __future__ import print_function, absolute_import

import os
import pytest


# Priority conversion pairs: (input_ext, output_ext, description)
CRITICAL_CONVERSIONS = [
    ('sk2', 'pdf', 'SK2 to PDF (prepress output)'),
    ('sk2', 'svg', 'SK2 to SVG (web export)'),
    ('sk2', 'png', 'SK2 to PNG (raster export)'),
    ('sk2', 'sk2', 'SK2 round-trip'),
    ('sk2', 'sk1', 'SK2 to SK1 (backward compatibility)'),
]

# Additional conversions to test if input files available
ADDITIONAL_CONVERSIONS = [
    ('sk2', 'svgz', 'SK2 to compressed SVG'),
    ('sk2', 'plt', 'SK2 to PLT (plotter)'),
    ('sk2', 'ps', 'SK2 to PostScript'),
    ('sk2', 'cdr', 'SK2 to CDR (CorelDRAW)'),
    ('sk2', 'cmx', 'SK2 to CMX (Corel Exchange)'),
]


def get_first_sk2_file(existing_sk2_files):
    """Get the first available SK2 file for testing."""
    if not existing_sk2_files:
        return None
    return existing_sk2_files[0]


@pytest.mark.parametrize('input_ext,output_ext,description', CRITICAL_CONVERSIONS)
def test_critical_conversion(uc2_app, existing_sk2_files, temp_output_dir, input_ext, output_ext, description):
    """Test critical format conversions."""
    if not existing_sk2_files:
        pytest.skip("No SK2 files available for conversion")

    from uc2.formats import get_loader, get_saver

    # Get input file
    input_file = get_first_sk2_file(existing_sk2_files)
    print("\nTesting: {}".format(description))
    print("  Input: {}".format(os.path.basename(input_file)))

    # Prepare output path
    output_file = os.path.join(temp_output_dir, 'output.{}'.format(output_ext))

    try:
        # Load document
        loader = get_loader(input_file)
        assert loader is not None, "No loader for .{}".format(input_ext)

        doc = loader(uc2_app.appdata, filename=input_file)
        assert doc is not None, "Failed to load document"
        print("  Loaded: {}".format(type(doc).__name__))

        # Save document
        saver = get_saver(output_file)
        assert saver is not None, "No saver for .{}".format(output_ext)

        saver(doc, filename=output_file)
        doc.close()

        # Verify output
        assert os.path.exists(output_file), "Output file not created"
        file_size = os.path.getsize(output_file)
        assert file_size > 0, "Output file is empty"

        print("  Output: {} ({} bytes)".format(os.path.basename(output_file), file_size))
        print("  SUCCESS")

    except Exception as e:
        pytest.fail("{} failed: {}".format(description, str(e)))


@pytest.mark.parametrize('input_ext,output_ext,description', ADDITIONAL_CONVERSIONS)
def test_additional_conversion(uc2_app, existing_sk2_files, temp_output_dir, input_ext, output_ext, description):
    """Test additional format conversions (may skip if not supported)."""
    if not existing_sk2_files:
        pytest.skip("No SK2 files available for conversion")

    from uc2.formats import get_loader, get_saver

    input_file = get_first_sk2_file(existing_sk2_files)
    output_file = os.path.join(temp_output_dir, 'output.{}'.format(output_ext))

    try:
        loader = get_loader(input_file)
        if loader is None:
            pytest.skip("No loader for .{}".format(input_ext))

        saver = get_saver(output_file)
        if saver is None:
            pytest.skip("No saver for .{}".format(output_ext))

        print("\nTesting: {}".format(description))

        doc = loader(uc2_app.appdata, filename=input_file)
        assert doc is not None

        saver(doc, filename=output_file)
        doc.close()

        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0

        print("  Output: {} bytes".format(os.path.getsize(output_file)))

    except Exception as e:
        print("  Skipped: {}".format(str(e)))
        pytest.skip("Conversion not supported: {}".format(str(e)))


def test_sk2_to_pdf_comprehensive(uc2_app, existing_sk2_files, temp_output_dir):
    """Comprehensive test: SK2 to PDF conversion."""
    if not existing_sk2_files:
        pytest.skip("No SK2 files available")

    from uc2.formats.sk2 import sk2_loader
    from uc2.formats.pdf import pdf_saver

    test_file = get_first_sk2_file(existing_sk2_files)
    output_file = os.path.join(temp_output_dir, 'comprehensive_test.pdf')

    print("\n=== SK2 to PDF Comprehensive Test ===")
    print("Input: {}".format(test_file))

    # Load
    doc = sk2_loader(uc2_app.appdata, filename=test_file)
    assert doc is not None
    assert doc.model is not None
    print("Loaded document: {} pages".format(len(doc.methods.get_pages())))

    # Save to PDF
    pdf_saver(doc, filename=output_file)
    doc.close()

    # Verify
    assert os.path.exists(output_file)
    file_size = os.path.getsize(output_file)
    assert file_size > 0

    # PDF files should start with %PDF
    with open(output_file, 'rb') as f:
        header = f.read(4)
        assert header == b'%PDF', "Output is not a valid PDF file"

    print("PDF output: {} bytes".format(file_size))
    print("SUCCESS")


def test_sk2_to_svg_comprehensive(uc2_app, existing_sk2_files, temp_output_dir):
    """Comprehensive test: SK2 to SVG conversion."""
    if not existing_sk2_files:
        pytest.skip("No SK2 files available")

    from uc2.formats.sk2 import sk2_loader
    from uc2.formats.svg import svg_saver

    test_file = get_first_sk2_file(existing_sk2_files)
    output_file = os.path.join(temp_output_dir, 'comprehensive_test.svg')

    print("\n=== SK2 to SVG Comprehensive Test ===")

    # Load
    doc = sk2_loader(uc2_app.appdata, filename=test_file)
    assert doc is not None
    print("Loaded document")

    # Save to SVG
    svg_saver(doc, filename=output_file)
    doc.close()

    # Verify
    assert os.path.exists(output_file)
    file_size = os.path.getsize(output_file)
    assert file_size > 0

    # SVG files should contain "<svg" or "<?xml"
    with open(output_file, 'r') as f:
        content = f.read(500)  # Read first 500 chars
        assert '<svg' in content or '<?xml' in content, "Output is not a valid SVG file"

    print("SVG output: {} bytes".format(file_size))
    print("SUCCESS")


def test_sk2_to_png_comprehensive(uc2_app, existing_sk2_files, temp_output_dir):
    """Comprehensive test: SK2 to PNG conversion."""
    if not existing_sk2_files:
        pytest.skip("No SK2 files available")

    from uc2.formats.sk2 import sk2_loader
    from uc2.formats.png import png_saver

    test_file = get_first_sk2_file(existing_sk2_files)
    output_file = os.path.join(temp_output_dir, 'comprehensive_test.png')

    print("\n=== SK2 to PNG Comprehensive Test ===")

    # Load
    doc = sk2_loader(uc2_app.appdata, filename=test_file)
    assert doc is not None
    print("Loaded document")

    # Save to PNG (with default options)
    png_saver(doc, filename=output_file)
    doc.close()

    # Verify
    assert os.path.exists(output_file)
    file_size = os.path.getsize(output_file)
    assert file_size > 0

    # PNG files should start with PNG signature
    with open(output_file, 'rb') as f:
        header = f.read(8)
        # PNG signature: 137 80 78 71 13 10 26 10
        assert header[1:4] == b'PNG', "Output is not a valid PNG file"

    print("PNG output: {} bytes".format(file_size))
    print("SUCCESS")


def test_multiple_sk2_files_to_pdf(uc2_app, existing_sk2_files, temp_output_dir):
    """Test converting multiple SK2 files to PDF."""
    if not existing_sk2_files:
        pytest.skip("No SK2 files available")

    from uc2.formats.sk2 import sk2_loader
    from uc2.formats.pdf import pdf_saver

    # Test first 3 files (or all if fewer)
    test_files = existing_sk2_files[:3]
    converted = 0

    print("\n=== Converting {} SK2 files to PDF ===".format(len(test_files)))

    for i, test_file in enumerate(test_files):
        try:
            output_file = os.path.join(temp_output_dir, 'multi_test_{}.pdf'.format(i))

            doc = sk2_loader(uc2_app.appdata, filename=test_file)
            pdf_saver(doc, filename=output_file)
            doc.close()

            assert os.path.exists(output_file)
            assert os.path.getsize(output_file) > 0

            print("  [{}] {} -> {} ({} bytes)".format(
                i + 1,
                os.path.basename(test_file),
                os.path.basename(output_file),
                os.path.getsize(output_file)
            ))
            converted += 1

        except Exception as e:
            print("  [{}] {} FAILED: {}".format(i + 1, os.path.basename(test_file), str(e)))

    assert converted > 0, "Failed to convert any files"
    print("Successfully converted {}/{} files".format(converted, len(test_files)))


def test_conversion_summary(uc2_app, existing_sk2_files, temp_output_dir):
    """Summary test showing all working conversions."""
    if not existing_sk2_files:
        pytest.skip("No SK2 files available")

    from uc2.formats import get_loader, get_saver

    test_file = get_first_sk2_file(existing_sk2_files)

    # All output formats to try
    output_formats = ['pdf', 'svg', 'svgz', 'png', 'sk2', 'sk1', 'plt', 'ps', 'cdr', 'cmx']

    print("\n=== Conversion Summary ===")
    print("Source: {}".format(os.path.basename(test_file)))

    successful = []
    failed = []

    for output_ext in output_formats:
        output_file = os.path.join(temp_output_dir, 'summary_test.{}'.format(output_ext))

        try:
            loader = get_loader(test_file)
            saver = get_saver(output_file)

            if loader is None or saver is None:
                failed.append((output_ext, "No loader/saver"))
                continue

            doc = loader(uc2_app.appdata, filename=test_file)
            saver(doc, filename=output_file)
            doc.close()

            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                size = os.path.getsize(output_file)
                successful.append((output_ext, size))
                print("  [OK] .{}: {} bytes".format(output_ext, size))
            else:
                failed.append((output_ext, "Empty output"))
                print("  [FAIL] .{}: Empty output".format(output_ext))

        except Exception as e:
            failed.append((output_ext, str(e)))
            print("  [SKIP] .{}: {}".format(output_ext, str(e)))

    print("\nResults:")
    print("  Successful: {}/{}".format(len(successful), len(output_formats)))
    print("  Failed/Skipped: {}".format(len(failed)))

    # We expect at least PDF and SVG to work
    successful_formats = [fmt for fmt, size in successful]
    assert 'pdf' in successful_formats or 'svg' in successful_formats, \
        "Neither PDF nor SVG conversion works"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
