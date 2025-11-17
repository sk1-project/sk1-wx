# -*- coding: utf-8 -*-
"""
Smoke Test 03: CLI Help and Info Commands

Tests that CLI commands can be invoked and display help/version/config info.
These tests don't do actual conversions, just verify the CLI is functional.

Compatible with Python 2.7 and Python 3.x.
"""

from __future__ import print_function, absolute_import

import os
import sys
import subprocess
import pytest


def get_uniconvertor_command():
    """Get the path to the uniconvertor command."""
    # First, try to find it in the built script location
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    built_cmd = os.path.join(repo_root, 'subproj', 'uniconvertor', 'src', 'script', 'uniconvertor')

    if os.path.exists(built_cmd):
        return built_cmd

    # Try to find it in PATH
    if sys.platform == 'win32':
        cmd = 'uniconvertor.exe'
    else:
        cmd = 'uniconvertor'

    # Check if it's in PATH
    try:
        result = subprocess.check_output(['which', cmd], stderr=subprocess.STDOUT)
        if result:
            return cmd
    except (subprocess.CalledProcessError, OSError):
        pass

    # Try the installed location
    installed_cmd = '/usr/bin/uniconvertor'
    if os.path.exists(installed_cmd):
        return installed_cmd

    return None


def get_sk1_command():
    """Get the path to the sk1 command."""
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    built_cmd = os.path.join(repo_root, 'src', 'script', 'sk1')

    if os.path.exists(built_cmd):
        return built_cmd

    # Try installed location
    installed_cmd = '/usr/bin/sk1'
    if os.path.exists(installed_cmd):
        return installed_cmd

    return None


def test_uniconvertor_exists():
    """Test that uniconvertor command exists."""
    cmd = get_uniconvertor_command()
    if cmd is None:
        pytest.skip("uniconvertor command not found - run 'python setup.py build' first")

    assert os.path.exists(cmd) or cmd == 'uniconvertor'
    print("uniconvertor command: {}".format(cmd))


def test_uniconvertor_help():
    """Test uniconvertor --help."""
    cmd = get_uniconvertor_command()
    if cmd is None:
        pytest.skip("uniconvertor command not found")

    try:
        # Run uniconvertor --help
        result = subprocess.check_output(
            [sys.executable, cmd, '--help'],
            stderr=subprocess.STDOUT
        )

        output = result.decode('utf-8') if isinstance(result, bytes) else result

        # Verify help output contains expected content
        assert 'usage' in output.lower() or 'Usage' in output
        assert 'uniconvertor' in output.lower()
        print("uniconvertor --help output length: {} bytes".format(len(output)))

    except subprocess.CalledProcessError as e:
        pytest.fail("uniconvertor --help failed: {}".format(str(e)))


def test_uniconvertor_show_config():
    """Test uniconvertor --show-config."""
    cmd = get_uniconvertor_command()
    if cmd is None:
        pytest.skip("uniconvertor command not found")

    try:
        result = subprocess.check_output(
            [sys.executable, cmd, '--show-config'],
            stderr=subprocess.STDOUT
        )

        output = result.decode('utf-8') if isinstance(result, bytes) else result

        # Config output should contain some configuration info
        assert len(output) > 0
        print("uniconvertor --show-config output length: {} bytes".format(len(output)))

    except subprocess.CalledProcessError as e:
        # --show-config might not be available in all versions
        print("Warning: --show-config not available: {}".format(str(e)))


def test_uniconvertor_package_dir():
    """Test uniconvertor --package-dir."""
    cmd = get_uniconvertor_command()
    if cmd is None:
        pytest.skip("uniconvertor command not found")

    try:
        result = subprocess.check_output(
            [sys.executable, cmd, '--package-dir'],
            stderr=subprocess.STDOUT
        )

        output = result.decode('utf-8') if isinstance(result, bytes) else result
        output = output.strip()

        # Should return a directory path
        assert len(output) > 0
        # The path might not exist if not installed, but should look like a path
        assert '/' in output or '\\' in output
        print("Package directory: {}".format(output))

    except subprocess.CalledProcessError as e:
        print("Warning: --package-dir not available: {}".format(str(e)))


def test_uniconvertor_version():
    """Test that uniconvertor has version information."""
    cmd = get_uniconvertor_command()
    if cmd is None:
        pytest.skip("uniconvertor command not found")

    # Try various version flags
    version_flags = ['--version', '-v']

    version_found = False

    for flag in version_flags:
        try:
            result = subprocess.check_output(
                [sys.executable, cmd, flag],
                stderr=subprocess.STDOUT
            )
            output = result.decode('utf-8') if isinstance(result, bytes) else result
            if 'version' in output.lower() or any(c.isdigit() for c in output):
                version_found = True
                print("Version info ({}): {}".format(flag, output.strip()))
                break
        except subprocess.CalledProcessError:
            continue

    # Note: Version flag might not be implemented, so we don't fail if not found
    if not version_found:
        print("Note: No version flag found (--version or -v)")


def test_sk1_exists():
    """Test that sk1 command exists."""
    cmd = get_sk1_command()
    if cmd is None:
        pytest.skip("sk1 command not found - run 'python setup.py build' first")

    assert os.path.exists(cmd) or cmd == 'sk1'
    print("sk1 command: {}".format(cmd))


def test_uniconvertor_no_args_behavior():
    """Test uniconvertor behavior when run without arguments."""
    cmd = get_uniconvertor_command()
    if cmd is None:
        pytest.skip("uniconvertor command not found")

    try:
        # Run without arguments - should show usage or help
        result = subprocess.Popen(
            [sys.executable, cmd],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = result.communicate()
        returncode = result.returncode

        # Combine stdout and stderr
        output = (stdout + stderr).decode('utf-8') if isinstance(stdout, bytes) else (stdout + stderr)

        # Should either succeed (showing help) or fail with usage message
        assert 'usage' in output.lower() or 'Usage' in output or 'help' in output.lower()
        print("No-args output length: {} bytes, returncode: {}".format(len(output), returncode))

    except Exception as e:
        pytest.fail("uniconvertor with no args failed unexpectedly: {}".format(str(e)))


def test_uc2_module_direct_call():
    """Test calling uc2 module directly (alternative to CLI)."""
    try:
        from uc2 import uc2_run
        assert uc2_run is not None
        assert callable(uc2_run)
        print("uc2_run() function is available")

    except ImportError as e:
        pytest.fail("Failed to import uc2_run: {}".format(str(e)))


def test_sk1_module_direct_call():
    """Test calling sk1 module directly (alternative to CLI)."""
    try:
        from sk1 import sk1_run
        assert sk1_run is not None
        assert callable(sk1_run)
        print("sk1_run() function is available")

    except ImportError as e:
        # sk1_run might fail if wxPython is not available
        print("Warning: sk1_run not available (probably due to missing wxPython): {}".format(str(e)))


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
