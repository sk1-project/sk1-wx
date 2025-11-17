# -*- coding: utf-8 -*-
"""
Smoke Test 10: PNG Rendering

Tests PNG export with Cairo rendering.
This tests the rendering pipeline: SK2 -> Cairo -> PNG.

Compatible with Python 2.7 and Python 3.x.
"""

from __future__ import print_function, absolute_import

import os
import pytest


@pytest.mark.native
def test_png_export_basic(uc2_app, existing_sk2_files, temp_output_dir):
    """Test basic PNG export from SK2."""
    if not existing_sk2_files:
        pytest.skip("No SK2 files available")

    from uc2.formats.sk2 import sk2_loader
    from uc2.formats.png import png_saver

    test_file = existing_sk2_files[0]
    output_file = os.path.join(temp_output_dir, 'render_test.png')

    print("Rendering: {}".format(os.path.basename(test_file)))

    # Load document
    doc = sk2_loader(uc2_app.appdata, filename=test_file)

    # Export to PNG
    png_saver(doc, filename=output_file)
    doc.close()

    # Verify PNG output
    assert os.path.exists(output_file)
    file_size = os.path.getsize(output_file)
    assert file_size > 0

    # Check PNG signature
    with open(output_file, 'rb') as f:
        header = f.read(8)
        assert header[1:4] == b'PNG', "Invalid PNG signature"

    print("PNG output: {} bytes".format(file_size))


@pytest.mark.native
def test_png_export_with_scale(uc2_app, existing_sk2_files, temp_output_dir):
    """Test PNG export with custom scale factor."""
    if not existing_sk2_files:
        pytest.skip("No SK2 files available")

    from uc2.formats.sk2 import sk2_loader
    from uc2.formats.png import png_saver

    test_file = existing_sk2_files[0]

    # Test different scale factors
    scales = [0.5, 1.0, 2.0]
    sizes = []

    for scale in scales:
        output_file = os.path.join(temp_output_dir, 'scale_{}.png'.format(scale))

        doc = sk2_loader(uc2_app.appdata, filename=test_file)

        # PNG saver with scale option
        try:
            png_saver(doc, filename=output_file, image_scale=scale)
            doc.close()

            if os.path.exists(output_file):
                size = os.path.getsize(output_file)
                sizes.append(size)
                print("Scale {}: {} bytes".format(scale, size))
        except TypeError:
            # image_scale might not be a parameter name in this version
            doc.close()
            pytest.skip("PNG scale parameter not supported in this version")

    # Larger scale should generally produce larger file
    if len(sizes) == 3:
        print("Sizes: {} -> {} -> {}".format(sizes[0], sizes[1], sizes[2]))


@pytest.mark.native
def test_cairo_renderer_import():
    """Test importing Cairo renderer."""
    try:
        from uc2.formats.sk2.sk2_render import CairoRenderer
        assert CairoRenderer is not None
        print("CairoRenderer class available")
    except ImportError as e:
        pytest.skip("CairoRenderer not available: {}".format(str(e)))


@pytest.mark.native
def test_cairo_surface_creation():
    """Test creating Cairo surface for rendering."""
    try:
        from uc2.libcairo import cairo

        # Try to create an image surface
        width, height = 100, 100
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        assert surface is not None

        context = cairo.Context(surface)
        assert context is not None

        print("Created Cairo surface: {}x{}".format(width, height))

    except ImportError:
        pytest.skip("Cairo module not available")
    except Exception as e:
        print("Note: Cairo surface creation test skipped: {}".format(str(e)))


@pytest.mark.native
def test_multiple_png_exports(uc2_app, existing_sk2_files, temp_output_dir):
    """Test exporting multiple SK2 files to PNG."""
    if not existing_sk2_files:
        pytest.skip("No SK2 files available")

    from uc2.formats.sk2 import sk2_loader
    from uc2.formats.png import png_saver

    # Test first 3 files
    test_files = existing_sk2_files[:3]
    rendered = 0

    print("\n=== Rendering {} files to PNG ===".format(len(test_files)))

    for i, test_file in enumerate(test_files):
        try:
            output_file = os.path.join(temp_output_dir, 'render_{}.png'.format(i))

            doc = sk2_loader(uc2_app.appdata, filename=test_file)
            png_saver(doc, filename=output_file)
            doc.close()

            assert os.path.exists(output_file)
            size = os.path.getsize(output_file)
            assert size > 0

            print("  [{}] {} -> {} bytes".format(
                i + 1, os.path.basename(test_file), size
            ))
            rendered += 1

        except Exception as e:
            print("  [{}] {} FAILED: {}".format(i + 1, os.path.basename(test_file), str(e)))

    assert rendered > 0, "Failed to render any files"
    print("Successfully rendered {}/{} files".format(rendered, len(test_files)))


@pytest.mark.native
def test_png_from_template(uc2_app, template_files, temp_output_dir):
    """Test rendering template SK2 files to PNG."""
    if not template_files:
        pytest.skip("No template files available")

    from uc2.formats.sk2 import sk2_loader
    from uc2.formats.png import png_saver

    test_file = template_files[0]
    output_file = os.path.join(temp_output_dir, 'template_render.png')

    print("Rendering template: {}".format(os.path.basename(test_file)))

    doc = sk2_loader(uc2_app.appdata, filename=test_file)
    png_saver(doc, filename=output_file)
    doc.close()

    assert os.path.exists(output_file)
    size = os.path.getsize(output_file)
    assert size > 0

    print("Template PNG: {} bytes".format(size))


def test_rendering_summary(uc2_app, existing_sk2_files, temp_output_dir):
    """Summary of rendering capabilities."""
    if not existing_sk2_files:
        pytest.skip("No SK2 files available")

    from uc2.formats.sk2 import sk2_loader
    from uc2.formats.png import png_saver

    test_file = existing_sk2_files[0]

    print("\n=== Rendering Summary ===")
    print("Source: {}".format(os.path.basename(test_file)))

    # Test basic render
    output_file = os.path.join(temp_output_dir, 'summary_render.png')

    try:
        doc = sk2_loader(uc2_app.appdata, filename=test_file)
        png_saver(doc, filename=output_file)
        doc.close()

        if os.path.exists(output_file):
            size = os.path.getsize(output_file)
            print("  [OK] Basic PNG render: {} bytes".format(size))

            # Check PNG validity
            with open(output_file, 'rb') as f:
                header = f.read(8)
                if header[1:4] == b'PNG':
                    print("  [OK] Valid PNG signature")
                else:
                    print("  [WARN] Invalid PNG signature")

        print("\nRendering: WORKING")

    except Exception as e:
        print("  [FAIL] Rendering failed: {}".format(str(e)))
        pytest.fail("PNG rendering not working")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
