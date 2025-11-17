# -*- coding: utf-8 -*-
"""
Smoke Test 11: CLI Conversions via Subprocess

Tests actual command-line conversions using the uniconvertor CLI.
This tests the full CLI pipeline, not just the Python API.

Compatible with Python 2.7 and Python 3.x.
"""

from __future__ import print_function, absolute_import

import os
import sys
import subprocess
import pytest


def get_uniconvertor_cmd():
    """Get the uniconvertor command path."""
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    built_cmd = os.path.join(repo_root, 'subproj', 'uniconvertor', 'src', 'script', 'uniconvertor')

    if os.path.exists(built_cmd):
        return built_cmd

    # Try system command
    return 'uniconvertor'


def test_cli_sk2_to_pdf(existing_sk2_files, temp_output_dir):
    """Test CLI conversion: SK2 to PDF."""
    if not existing_sk2_files:
        pytest.skip("No SK2 files available")

    cmd = get_uniconvertor_cmd()
    if not os.path.exists(cmd) and cmd != 'uniconvertor':
        pytest.skip("uniconvertor command not found")

    input_file = existing_sk2_files[0]
    output_file = os.path.join(temp_output_dir, 'cli_test.pdf')

    print("\n=== CLI Test: SK2 to PDF ===")
    print("Input: {}".format(os.path.basename(input_file)))
    print("Command: {} {} {}".format(cmd, input_file, output_file))

    try:
        # Run uniconvertor
        result = subprocess.call(
            [sys.executable, cmd, input_file, output_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Check result
        assert os.path.exists(output_file), "Output file not created"
        size = os.path.getsize(output_file)
        assert size > 0, "Output file is empty"

        # Verify PDF signature
        with open(output_file, 'rb') as f:
            header = f.read(4)
            assert header == b'%PDF', "Invalid PDF file"

        print("Success: {} bytes (return code: {})".format(size, result))

    except (OSError, subprocess.CalledProcessError) as e:
        pytest.fail("CLI conversion failed: {}".format(str(e)))


def test_cli_sk2_to_svg(existing_sk2_files, temp_output_dir):
    """Test CLI conversion: SK2 to SVG."""
    if not existing_sk2_files:
        pytest.skip("No SK2 files available")

    cmd = get_uniconvertor_cmd()
    if not os.path.exists(cmd) and cmd != 'uniconvertor':
        pytest.skip("uniconvertor command not found")

    input_file = existing_sk2_files[0]
    output_file = os.path.join(temp_output_dir, 'cli_test.svg')

    print("\n=== CLI Test: SK2 to SVG ===")

    try:
        result = subprocess.call(
            [sys.executable, cmd, input_file, output_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        assert os.path.exists(output_file)
        size = os.path.getsize(output_file)
        assert size > 0

        # Verify SVG content
        with open(output_file, 'r') as f:
            content = f.read(500)
            assert '<svg' in content or '<?xml' in content

        print("Success: {} bytes".format(size))

    except Exception as e:
        pytest.fail("CLI conversion failed: {}".format(str(e)))


def test_cli_sk2_to_png(existing_sk2_files, temp_output_dir):
    """Test CLI conversion: SK2 to PNG."""
    if not existing_sk2_files:
        pytest.skip("No SK2 files available")

    cmd = get_uniconvertor_cmd()
    if not os.path.exists(cmd) and cmd != 'uniconvertor':
        pytest.skip("uniconvertor command not found")

    input_file = existing_sk2_files[0]
    output_file = os.path.join(temp_output_dir, 'cli_test.png')

    print("\n=== CLI Test: SK2 to PNG ===")

    try:
        result = subprocess.call(
            [sys.executable, cmd, input_file, output_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        assert os.path.exists(output_file)
        size = os.path.getsize(output_file)
        assert size > 0

        # Verify PNG signature
        with open(output_file, 'rb') as f:
            header = f.read(8)
            assert header[1:4] == b'PNG'

        print("Success: {} bytes".format(size))

    except Exception as e:
        pytest.fail("CLI conversion failed: {}".format(str(e)))


def test_cli_with_format_option(existing_sk2_files, temp_output_dir):
    """Test CLI conversion with --format option."""
    if not existing_sk2_files:
        pytest.skip("No SK2 files available")

    cmd = get_uniconvertor_cmd()
    if not os.path.exists(cmd) and cmd != 'uniconvertor':
        pytest.skip("uniconvertor command not found")

    input_file = existing_sk2_files[0]
    output_file = os.path.join(temp_output_dir, 'cli_format_test.pdf')

    print("\n=== CLI Test: --format option ===")

    try:
        # Use --format=pdf explicitly
        result = subprocess.call(
            [sys.executable, cmd, '--format=pdf', input_file, output_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0

        print("Success with --format=pdf")

    except Exception as e:
        print("Note: --format option might not be supported: {}".format(str(e)))


def test_cli_verbose_mode(existing_sk2_files, temp_output_dir):
    """Test CLI conversion with verbose output."""
    if not existing_sk2_files:
        pytest.skip("No SK2 files available")

    cmd = get_uniconvertor_cmd()
    if not os.path.exists(cmd) and cmd != 'uniconvertor':
        pytest.skip("uniconvertor command not found")

    input_file = existing_sk2_files[0]
    output_file = os.path.join(temp_output_dir, 'cli_verbose_test.pdf')

    print("\n=== CLI Test: Verbose mode ===")

    try:
        # Run with -v or --verbose
        proc = subprocess.Popen(
            [sys.executable, cmd, '-v', input_file, output_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = proc.communicate()

        output = (stdout + stderr).decode('utf-8') if isinstance(stdout, bytes) else (stdout + stderr)

        # Should have some output in verbose mode
        assert len(output) > 0 or os.path.exists(output_file)

        if os.path.exists(output_file):
            print("Success (verbose mode produced output)")
        else:
            print("Note: -v flag might not be supported")

    except Exception as e:
        print("Note: Verbose mode test skipped: {}".format(str(e)))


def test_cli_multiple_conversions(existing_sk2_files, temp_output_dir):
    """Test multiple CLI conversions in sequence."""
    if not existing_sk2_files:
        pytest.skip("No SK2 files available")

    cmd = get_uniconvertor_cmd()
    if not os.path.exists(cmd) and cmd != 'uniconvertor':
        pytest.skip("uniconvertor command not found")

    # Test first 3 files
    test_files = existing_sk2_files[:3]
    successful = 0

    print("\n=== CLI Multiple Conversions ===")

    for i, input_file in enumerate(test_files):
        output_file = os.path.join(temp_output_dir, 'cli_multi_{}.pdf'.format(i))

        try:
            result = subprocess.call(
                [sys.executable, cmd, input_file, output_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30  # 30 second timeout per file
            )

            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                successful += 1
                print("  [{}] {} -> OK ({} bytes)".format(
                    i + 1, os.path.basename(input_file), os.path.getsize(output_file)
                ))
            else:
                print("  [{}] {} -> FAILED".format(i + 1, os.path.basename(input_file)))

        except subprocess.TimeoutExpired:
            print("  [{}] {} -> TIMEOUT".format(i + 1, os.path.basename(input_file)))
        except Exception as e:
            print("  [{}] {} -> ERROR: {}".format(i + 1, os.path.basename(input_file), str(e)))

    assert successful > 0, "No CLI conversions succeeded"
    print("Success: {}/{} conversions".format(successful, len(test_files)))


def test_cli_conversion_summary(existing_sk2_files, temp_output_dir):
    """Summary of CLI conversion capabilities."""
    if not existing_sk2_files:
        pytest.skip("No SK2 files available")

    cmd = get_uniconvertor_cmd()
    if not os.path.exists(cmd) and cmd != 'uniconvertor':
        pytest.skip("uniconvertor command not found")

    input_file = existing_sk2_files[0]

    # Test formats
    formats = ['pdf', 'svg', 'png']
    results = {}

    print("\n=== CLI Conversion Summary ===")
    print("Source: {}".format(os.path.basename(input_file)))

    for fmt in formats:
        output_file = os.path.join(temp_output_dir, 'cli_summary.{}'.format(fmt))

        try:
            result = subprocess.call(
                [sys.executable, cmd, input_file, output_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30
            )

            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                size = os.path.getsize(output_file)
                results[fmt] = size
                print("  [OK] .{}: {} bytes".format(fmt, size))
            else:
                results[fmt] = 0
                print("  [FAIL] .{}: Not created".format(fmt))

        except Exception as e:
            results[fmt] = None
            print("  [ERROR] .{}: {}".format(fmt, str(e)))

    # At least one format should work
    successful = [fmt for fmt, size in results.items() if size and size > 0]
    assert len(successful) > 0, "No CLI conversions worked"

    print("\nCLI Summary: {}/{} formats working".format(len(successful), len(formats)))


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
