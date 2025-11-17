# -*- coding: utf-8 -*-
"""
Pytest configuration and shared fixtures for sK1 smoke tests.

This file provides shared fixtures and configuration for all smoke tests.
It is compatible with both Python 2.7 and Python 3.x.
"""

from __future__ import print_function, absolute_import

import os
import sys
import tempfile
import shutil

import pytest


# Ensure the source directory is in the path
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(REPO_ROOT, 'src')
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# Also add the build directory for native extensions
# The build directory name varies by platform and Python version
BUILD_DIR = os.path.join(REPO_ROOT, 'build')
if os.path.exists(BUILD_DIR):
    # Find lib.* directories in build/
    import glob
    lib_dirs = glob.glob(os.path.join(BUILD_DIR, 'lib.*'))
    if lib_dirs:
        # Use the first (and usually only) lib directory
        build_lib = lib_dirs[0]
        if build_lib not in sys.path:
            sys.path.insert(0, build_lib)
            print("Added build directory to path: {}".format(build_lib))


@pytest.fixture(scope='session')
def repo_root():
    """Return the repository root directory."""
    return REPO_ROOT


@pytest.fixture(scope='session')
def src_dir():
    """Return the src directory."""
    return SRC_DIR


@pytest.fixture(scope='session')
def resources_dir():
    """Return the resources directory with existing SK2 files."""
    return os.path.join(REPO_ROOT, 'resources')


@pytest.fixture(scope='session')
def test_data_dir():
    """Return the test data directory."""
    return os.path.join(REPO_ROOT, 'tests', 'test_data')


@pytest.fixture(scope='session')
def existing_sk2_files(resources_dir):
    """Return a list of existing SK2 files from resources directory."""
    sk2_files = []

    # Recursively find all .sk2 files in resources/
    for root, dirs, files in os.walk(resources_dir):
        for filename in files:
            if filename.endswith('.sk2'):
                sk2_files.append(os.path.join(root, filename))

    return sk2_files


@pytest.fixture(scope='session')
def template_files():
    """Return paths to template SK2 files."""
    templates_dir = os.path.join(REPO_ROOT, 'src', 'sk1', 'share', 'templates')
    templates = []

    if os.path.exists(templates_dir):
        for filename in os.listdir(templates_dir):
            if filename.endswith('.sk2'):
                templates.append(os.path.join(templates_dir, filename))

    return templates


@pytest.fixture
def temp_output_dir():
    """Create a temporary directory for test outputs, cleaned up after test."""
    temp_dir = tempfile.mkdtemp(prefix='sk1_test_')
    yield temp_dir
    # Cleanup
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


@pytest.fixture
def temp_file():
    """Create a temporary file, cleaned up after test."""
    fd, path = tempfile.mkstemp(prefix='sk1_test_')
    os.close(fd)
    yield path
    # Cleanup
    if os.path.exists(path):
        os.unlink(path)


@pytest.fixture(scope='session')
def uc2_app():
    """Initialize and return a UC2 application instance (session-scoped)."""
    # Import here to avoid issues if uc2 is not built yet
    try:
        from uc2 import uc2_init
        app = uc2_init()
        yield app
    except ImportError:
        pytest.skip("UC2 not available - run 'python setup.py build' first")


@pytest.fixture(scope='session')
def existing_test_data():
    """Return paths to existing test data from uniconvertor tests."""
    base_dir = os.path.join(REPO_ROOT, 'subproj', 'uniconvertor', 'tests', 'unit-tests')

    test_data = {
        'cms_data': os.path.join(base_dir, 'cms_tests', 'cms_data'),
        'img_data': os.path.join(base_dir, '_libimg_tests', 'img_data'),
        'image_data': os.path.join(base_dir, 'image_tests', 'image_data'),
        'uc2_data': os.path.join(base_dir, 'uc2_tests', 'uc2_data'),
    }

    # Filter to only existing directories
    return {k: v for k, v in test_data.items() if os.path.exists(v)}


@pytest.fixture(scope='session')
def has_display():
    """Check if a display is available (for GUI tests)."""
    return 'DISPLAY' in os.environ or sys.platform == 'win32' or sys.platform == 'darwin'


def pytest_configure(config):
    """Pytest configuration hook."""
    # Add custom markers
    config.addinivalue_line(
        "markers", "gui: marks tests that require a display (deselect with '-m \"not gui\"')"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "native: marks tests that require native extensions"
    )
