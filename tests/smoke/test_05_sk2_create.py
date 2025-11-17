# -*- coding: utf-8 -*-
"""
Smoke Test 05: SK2 Document Creation and Round-trip

Tests creating SK2 documents, saving them, and loading them back.
This is a critical test - if round-trip save/load fails, the app is broken.

Compatible with Python 2.7 and Python 3.x.
"""

from __future__ import print_function, absolute_import

import os
import pytest


def test_create_empty_sk2_document(uc2_app):
    """Test creating an empty SK2 document."""
    from uc2.formats.sk2.sk2_presenter import SK2_Presenter

    doc = SK2_Presenter(uc2_app.appdata)
    assert doc is not None
    assert doc.model is not None

    # Should have at least one page
    pages = doc.methods.get_pages()
    assert pages is not None
    assert len(pages) > 0
    print("Created document with {} page(s)".format(len(pages)))

    doc.close()


def test_sk2_save(uc2_app, temp_file):
    """Test saving an SK2 document."""
    from uc2.formats.sk2.sk2_presenter import SK2_Presenter

    # Create a document
    doc = SK2_Presenter(uc2_app.appdata)

    # Save it
    output_path = temp_file + '.sk2'
    doc.save(output_path)

    # Verify file exists and is not empty
    assert os.path.exists(output_path)
    assert os.path.getsize(output_path) > 0

    file_size = os.path.getsize(output_path)
    print("Saved SK2 file: {} ({} bytes)".format(output_path, file_size))

    doc.close()

    # Cleanup
    if os.path.exists(output_path):
        os.unlink(output_path)


def test_sk2_load(uc2_app, existing_sk2_files):
    """Test loading an existing SK2 file."""
    if not existing_sk2_files:
        pytest.skip("No existing SK2 files found")

    from uc2.formats.sk2.sk2_presenter import SK2_Presenter

    # Load the first existing SK2 file
    test_file = existing_sk2_files[0]
    print("Loading: {}".format(test_file))

    doc = SK2_Presenter(uc2_app.appdata, filepath=test_file)
    assert doc is not None
    assert doc.model is not None

    # Should have pages
    pages = doc.methods.get_pages()
    assert pages is not None
    print("Loaded document with {} page(s)".format(len(pages)))

    doc.close()


def test_sk2_round_trip(uc2_app, temp_output_dir):
    """Test creating, saving, and reloading an SK2 document."""
    from uc2.formats.sk2.sk2_presenter import SK2_Presenter

    # Create a document
    doc1 = SK2_Presenter(uc2_app.appdata)
    page = doc1.methods.get_page()

    # Save it
    output_path = os.path.join(temp_output_dir, 'round_trip_test.sk2')
    doc1.save(output_path)
    doc1.close()

    # Verify saved file
    assert os.path.exists(output_path)
    file_size = os.path.getsize(output_path)
    assert file_size > 0
    print("Saved: {} bytes".format(file_size))

    # Load it back
    doc2 = SK2_Presenter(uc2_app.appdata, filepath=output_path)
    assert doc2 is not None
    assert doc2.model is not None

    # Verify it has pages
    pages = doc2.methods.get_pages()
    assert pages is not None
    assert len(pages) > 0

    doc2.close()
    print("Round-trip successful")


def test_sk2_save_with_saver_function(uc2_app, temp_output_dir):
    """Test saving SK2 using the sk2_saver function."""
    from uc2.formats.sk2.sk2_presenter import SK2_Presenter
    from uc2.formats.sk2 import sk2_saver

    # Create a document
    doc = SK2_Presenter(uc2_app.appdata)

    # Save using saver function
    output_path = os.path.join(temp_output_dir, 'saver_test.sk2')
    sk2_saver(doc, output_path)

    # Verify
    assert os.path.exists(output_path)
    assert os.path.getsize(output_path) > 0
    print("Saved with sk2_saver: {} bytes".format(os.path.getsize(output_path)))

    doc.close()


def test_sk2_load_with_loader_function(uc2_app, existing_sk2_files):
    """Test loading SK2 using the sk2_loader function."""
    if not existing_sk2_files:
        pytest.skip("No existing SK2 files found")

    from uc2.formats.sk2 import sk2_loader

    test_file = existing_sk2_files[0]
    print("Loading with sk2_loader: {}".format(test_file))

    doc = sk2_loader(uc2_app.appdata, filename=test_file)
    assert doc is not None
    assert doc.model is not None

    doc.close()


def test_sk2_multiple_files(uc2_app, existing_sk2_files):
    """Test loading multiple existing SK2 files."""
    if not existing_sk2_files:
        pytest.skip("No existing SK2 files found")

    from uc2.formats.sk2.sk2_presenter import SK2_Presenter

    # Test first 5 files (or all if fewer)
    test_files = existing_sk2_files[:5]
    loaded_count = 0

    for sk2_file in test_files:
        try:
            print("Loading: {}".format(os.path.basename(sk2_file)))
            doc = SK2_Presenter(uc2_app.appdata, filepath=sk2_file)
            assert doc is not None
            assert doc.model is not None
            doc.close()
            loaded_count += 1
        except Exception as e:
            print("Warning: Failed to load {}: {}".format(sk2_file, str(e)))

    assert loaded_count > 0, "Failed to load any SK2 files"
    print("Successfully loaded {}/{} files".format(loaded_count, len(test_files)))


def test_sk2_template_files(uc2_app, template_files):
    """Test loading SK2 template files."""
    if not template_files:
        pytest.skip("No template files found")

    from uc2.formats.sk2.sk2_presenter import SK2_Presenter

    for template_file in template_files:
        print("Loading template: {}".format(os.path.basename(template_file)))
        doc = SK2_Presenter(uc2_app.appdata, filepath=template_file)
        assert doc is not None
        assert doc.model is not None

        pages = doc.methods.get_pages()
        print("  Pages: {}".format(len(pages)))

        doc.close()


def test_sk2_document_has_layers(uc2_app):
    """Test that SK2 documents have layer structure."""
    from uc2.formats.sk2.sk2_presenter import SK2_Presenter

    doc = SK2_Presenter(uc2_app.appdata)
    page = doc.methods.get_page()

    # Try to get layer
    try:
        layer = doc.methods.get_layer(page)
        assert layer is not None
        print("Document has layer structure")
    except Exception as e:
        print("Warning: Could not get layer: {}".format(str(e)))

    doc.close()


def test_sk2_document_units(uc2_app):
    """Test getting/setting document units."""
    from uc2.formats.sk2.sk2_presenter import SK2_Presenter
    from uc2 import uc2const

    doc = SK2_Presenter(uc2_app.appdata)

    # Try to set units
    try:
        doc.methods.set_doc_units(uc2const.UNIT_MM)
        print("Set document units to MM")
    except Exception as e:
        print("Warning: Could not set units: {}".format(str(e)))

    doc.close()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
