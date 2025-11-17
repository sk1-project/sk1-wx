# -*- coding: utf-8 -*-
"""
Smoke Test 13: GUI Tests

Tests GUI initialization. Requires X11/display or Xvfb.
These tests will be skipped if no display is available.

Compatible with Python 2.7 and Python 3.x.
"""

from __future__ import print_function, absolute_import

import os
import sys
import pytest


@pytest.mark.gui
def test_wxpython_import(has_display):
    """Test importing wxPython."""
    if not has_display:
        pytest.skip("No display available for GUI tests")

    try:
        import wx
        assert wx is not None
        print("wxPython version: {}".format(wx.version()))

    except ImportError as e:
        pytest.skip("wxPython not installed: {}".format(str(e)))


@pytest.mark.gui
def test_wal_import(has_display):
    """Test importing WAL (Widget Abstraction Layer)."""
    if not has_display:
        pytest.skip("No display available for GUI tests")

    try:
        import wal
        assert wal is not None
        print("WAL imported successfully")

    except ImportError as e:
        pytest.skip("WAL not available: {}".format(str(e)))


@pytest.mark.gui
def test_sk1_application_import(has_display):
    """Test importing SK1 application class."""
    if not has_display:
        pytest.skip("No display available for GUI tests")

    try:
        from sk1.application import SK1Application
        assert SK1Application is not None
        print("SK1Application class available")

    except ImportError as e:
        pytest.skip("SK1 application not available: {}".format(str(e)))


@pytest.mark.gui
def test_sk1_parts_import(has_display):
    """Test importing SK1 UI parts."""
    if not has_display:
        pytest.skip("No display available for GUI tests")

    try:
        # Try to import some UI components
        from sk1.parts import menubar
        from sk1.parts import toolbar

        assert menubar is not None
        assert toolbar is not None
        print("SK1 UI parts imported successfully")

    except ImportError as e:
        pytest.skip("SK1 UI parts not available: {}".format(str(e)))


@pytest.mark.gui
def test_sk1_dialogs_import(has_display):
    """Test importing SK1 dialogs."""
    if not has_display:
        pytest.skip("No display available for GUI tests")

    try:
        from sk1.dialogs import aboutdlg
        assert aboutdlg is not None
        print("SK1 dialogs imported successfully")

    except ImportError as e:
        pytest.skip("SK1 dialogs not available: {}".format(str(e)))


@pytest.mark.gui
def test_sk1_context_import(has_display):
    """Test importing SK1 context panels."""
    if not has_display:
        pytest.skip("No display available for GUI tests")

    try:
        # Try to import context panels
        import sk1.context
        print("SK1 context panels module available")

    except ImportError as e:
        pytest.skip("SK1 context panels not available: {}".format(str(e)))


@pytest.mark.gui
def test_create_wx_app(has_display):
    """Test creating a minimal wx.App (doesn't start event loop)."""
    if not has_display:
        pytest.skip("No display available for GUI tests")

    try:
        import wx

        # Create app without starting main loop
        app = wx.App(False)
        assert app is not None
        print("Created wx.App successfully")

        # Clean up
        app.Destroy()

    except ImportError as e:
        pytest.skip("wxPython not available: {}".format(str(e)))
    except Exception as e:
        pytest.fail("Failed to create wx.App: {}".format(str(e)))


@pytest.mark.gui
def test_sk1_config_import(has_display):
    """Test SK1 configuration module (doesn't require display)."""
    # This test doesn't actually need display, but grouped with GUI tests
    try:
        from sk1 import app_conf
        assert app_conf is not None
        print("SK1 configuration module available")

    except ImportError as e:
        pytest.fail("SK1 config not available: {}".format(str(e)))


@pytest.mark.gui
def test_sk1_document_without_gui():
    """Test SK1 document presenter without full GUI (should work headless)."""
    # This uses SK1Presenter which should work without GUI
    try:
        from sk1.document.presenter import SK1Presenter
        from uc2 import uc2_init

        # This should work even without display
        app = uc2_init()
        # SK1Presenter might need GUI context, so we just test import
        assert SK1Presenter is not None
        print("SK1Presenter class available")

    except ImportError as e:
        pytest.skip("SK1Presenter not available: {}".format(str(e)))


def test_gui_summary(has_display):
    """Summary of GUI component availability."""
    print("\n=== GUI Components Summary ===")
    print("Display available: {}".format(has_display))

    if not has_display:
        print("Note: GUI tests will be skipped (no display)")
        print("To run GUI tests:")
        print("  - On Linux: Start Xvfb or use pytest-xvfb")
        print("  - On macOS: Ensure X11/XQuartz is running")
        print("  - On Windows: Display should be automatically available")
        return

    components = {
        'wxPython': 'wx',
        'WAL': 'wal',
        'SK1 Application': 'sk1.application',
        'SK1 Document': 'sk1.document',
        'SK1 Parts': 'sk1.parts',
        'SK1 Dialogs': 'sk1.dialogs',
    }

    available = []
    unavailable = []

    for name, module_path in components.items():
        try:
            __import__(module_path)
            available.append(name)
            print("  [OK] {}".format(name))
        except ImportError:
            unavailable.append(name)
            print("  [MISSING] {}".format(name))

    print("\nGUI Components: {}/{} available".format(len(available), len(components)))

    if unavailable:
        print("Missing components: {}".format(', '.join(unavailable)))


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
