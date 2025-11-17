# sK1/UniConvertor Smoke Tests

Comprehensive smoke test suite for validating sK1/UniConvertor functionality during the Python 2.7 → Python 3 migration.

## Purpose

These tests serve two critical purposes:

1. **Baseline Validation (Python 2.7)**: Capture current behavior of the application running on Python 2.7.18
2. **Migration Validation (Python 3.x)**: Verify that all core functionality works identically after migrating to Python 3

The tests are designed to be **compatible with both Python 2.7 and Python 3.x** without modification.

## Prerequisites

### 1. Build the Project

Before running tests, you **must** build the project to compile native extensions and set up submodules:

```bash
python setup.py build
```

This will:
- Clone subprojects (uniconvertor, wal, build-utils)
- Create symlinks (src/uc2, src/wal, utils)
- Compile native C extensions (_cms, _libcairo, _libpango, _libimg)
- Build translations

### 2. Install Test Dependencies

```bash
# For Python 2.7
pyenv shell 2.7.18
pip install -r requirements-test.txt

# For Python 3.x (after migration)
pyenv shell 3.14.0
pip install -r requirements-test.txt
```

## Test Structure

```
tests/
├── conftest.py                     # pytest configuration & fixtures
├── smoke/
│   ├── test_01_imports.py          # Core module imports
│   ├── test_02_native_extensions.py # Native C extensions
│   ├── test_03_cli_help.py         # CLI help/version
│   ├── test_04_uc2_api.py          # UC2 API initialization
│   ├── test_05_sk2_create.py       # Document creation & round-trip
│   ├── test_06_format_loaders.py   # All 30+ format loaders
│   ├── test_07_format_savers.py    # All format savers
│   ├── test_08_conversions.py      # Cross-format conversions
│   ├── test_09_cms.py              # Color management (CMYK workflow)
│   ├── test_10_rendering.py        # PNG rendering with Cairo
│   ├── test_11_cli_convert.py      # CLI conversions via subprocess
│   ├── test_12_existing_tests.py   # Run existing UC2 unit tests
│   └── test_13_gui.py              # GUI initialization (requires X11)
├── run_smoke.sh                    # Convenient test runner
└── README.md                       # This file
```

## Running Tests

### Quick Start

```bash
# Run all smoke tests
./tests/run_smoke.sh

# Run with verbose output
./tests/run_smoke.sh -vv

# Run only fast tests (skip slow tests)
./tests/run_smoke.sh --quick

# Run without GUI tests (no X11/display needed)
./tests/run_smoke.sh --no-gui

# Run only critical tests (fast, no GUI)
./tests/run_smoke.sh --only-critical

# Exit on first failure
./tests/run_smoke.sh -x
```

### Using pytest Directly

```bash
# All smoke tests
pytest tests/smoke/ -v

# Specific test file
pytest tests/smoke/test_08_conversions.py -v

# Specific test function
pytest tests/smoke/test_08_conversions.py::test_sk2_to_pdf_comprehensive -v

# Skip slow tests
pytest tests/smoke/ -v -m "not slow"

# Skip GUI tests
pytest tests/smoke/ -v -m "not gui"

# Only native extension tests
pytest tests/smoke/ -v -m "native"

# With coverage
pytest tests/smoke/ -v --cov=src --cov=subproj

# Stop on first failure
pytest tests/smoke/ -v -x
```

## Test Categories

### Test Markers

Tests are marked with the following pytest markers:

- `@pytest.mark.native` - Tests requiring native C extensions
- `@pytest.mark.gui` - Tests requiring X11/display
- `@pytest.mark.slow` - Tests that may take longer to run

### Critical Path Tests (Must Pass)

1. **test_01_imports.py** - All core modules import
2. **test_02_native_extensions.py** - All 4 native extensions load
3. **test_04_uc2_api.py** - UC2 API initializes
4. **test_05_sk2_create.py** - SK2 save/load round-trip works
5. **test_08_conversions.py** - Critical format conversions work

### Comprehensive Coverage

6. **test_06_format_loaders.py** - All 30+ format loaders available
7. **test_07_format_savers.py** - All format savers available
8. **test_09_cms.py** - Color management (RGB↔CMYK transforms)
9. **test_10_rendering.py** - PNG export with Cairo rendering
10. **test_11_cli_convert.py** - CLI conversions work via subprocess

## Test Data

The tests use existing files from the repository:

- **SK2 Files**: `resources/**/*.sk2` (30+ files)
- **Templates**: `src/sk1/share/templates/*.sk2`
- **CMS Test Data**: `subproj/uniconvertor/tests/unit-tests/cms_tests/cms_data/`
- **Image Test Data**: `subproj/uniconvertor/tests/unit-tests/_libimg_tests/img_data/`

No additional test files need to be created.

## Expected Results

### Python 2.7 (Current)

All tests should pass on Python 2.7.18. If any fail, there may be build or dependency issues.

```bash
pyenv shell 2.7.18
python setup.py build
pip install -r requirements-test.txt
pytest tests/smoke/ -v
```

Expected: **~100+ tests passing** (exact count depends on available test data)

### Python 3.x (After Migration)

After migrating to Python 3, the same tests should pass with identical results.

```bash
pyenv shell 3.14.0
python setup.py build
pip install -r requirements-test.txt
pytest tests/smoke/ -v
```

Expected: **Same pass rate as Python 2.7**

Any differences indicate migration regressions that must be fixed.

## GUI Testing

GUI tests (test_13_gui.py) require a display.

### Linux

```bash
# Option 1: Use Xvfb (virtual display) - Python 3+ only
# Note: pytest-xvfb is not compatible with Python 2.7
sudo apt-get install xvfb
xvfb-run pytest tests/smoke/ -v

# Option 2: Use pytest-xvfb (Python 3+ only)
# For Python 3:
pip install pytest-xvfb
pytest tests/smoke/ -v  # Will use Xvfb automatically

# Option 3: Skip GUI tests (RECOMMENDED for Python 2.7)
pytest tests/smoke/ -v -m "not gui"
```

### macOS

```bash
# Ensure X11/XQuartz is running
# GUI tests should work if DISPLAY is set

# Or skip GUI tests
pytest tests/smoke/ -v -m "not gui"
```

### Windows

Display should be available automatically. GUI tests should work.

## Common Issues

### Issue: "No module named uc2"

**Cause**: Project not built
**Solution**:
```bash
python setup.py build
```

### Issue: "ImportError: No module named _cms"

**Cause**: Native extensions not compiled
**Solution**:
```bash
# Install build dependencies
sudo apt-get install libcairo2-dev liblcms2-dev libmagickwand-dev libpango1.0-dev python-dev

# Rebuild
python setup.py build
```

### Issue: "No SK2 files found"

**Cause**: Resources directory missing
**Solution**:
```bash
# Check if resources exist
ls resources/*.sk2

# If missing, ensure you're in the repo root
cd /path/to/sk1-wx
```

### Issue: GUI tests fail with "cannot open display"

**Cause**: No X11 display available
**Solution**:
```bash
# Skip GUI tests (RECOMMENDED for Python 2.7)
pytest tests/smoke/ -v -m "not gui"

# Or use Xvfb (Python 3 only, not available on Python 2.7)
xvfb-run pytest tests/smoke/ -v
```

### Issue: "SyntaxError: invalid syntax" in pyvirtualdisplay

**Cause**: pytest-xvfb requires Python 3+ (not compatible with Python 2.7)
**Solution**:
```bash
# Uninstall pytest-xvfb on Python 2.7
pip uninstall -y pytest-xvfb pyvirtualdisplay

# Skip GUI tests on Python 2.7
pytest tests/smoke/ -v -m "not gui"

# Or if you have a real display (e.g., macOS with XQuartz)
pytest tests/smoke/ -v  # GUI tests will run if DISPLAY is set
```

## Interpreting Results

### All Tests Pass ✓

Great! The application is working correctly.

### Some Tests Skipped

Normal. Tests are skipped when:
- GUI tests run without display: `SKIPPED (No display available)`
- Format not supported: `SKIPPED (Saver for CDR not available)`
- Test data missing: `SKIPPED (No SK2 files available)`

### Tests Fail ✗

**Critical** - Must be fixed. Check:

1. **Build errors**: Run `python setup.py build` again
2. **Dependency errors**: Install missing system libraries
3. **Actual bugs**: The test found a real issue

## Test Maintenance

### Adding New Tests

1. Create test file in `tests/smoke/`
2. Use `@pytest.mark.*` for categorization
3. Ensure Python 2/3 compatibility:
   - Use `from __future__ import print_function, absolute_import`
   - No f-strings
   - No pathlib
   - No type hints in function signatures

### Python 2/3 Compatibility Guidelines

```python
# ✓ Good (works on both)
from __future__ import print_function, absolute_import
import os
path = os.path.join('dir', 'file')
message = "Value: {}".format(value)

# ✗ Bad (Python 3 only)
path = Path('dir') / 'file'
message = f"Value: {value}"
def func(x: int) -> str: pass
```

## Continuous Integration

For CI/CD pipelines:

```yaml
# Example .github/workflows/smoke-tests.yml
name: Smoke Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["2.7", "3.14"]

    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          sudo apt-get install -y libcairo2-dev liblcms2-dev \
            libmagickwand-dev libpango1.0-dev python-dev xvfb
          pip install -r requirements-test.txt

      - name: Build project
        run: python setup.py build

      - name: Run smoke tests
        run: xvfb-run pytest tests/smoke/ -v -m "not slow"
```

## Questions?

If you encounter issues:

1. Check that `python setup.py build` completes without errors
2. Verify all dependencies are installed (see CLAUDE.md)
3. Review test output for specific error messages
4. Check if the issue occurs on both Python 2.7 and Python 3

## Summary

These smoke tests provide **comprehensive coverage** of:

- ✓ Module imports
- ✓ Native extensions (4 critical C libraries)
- ✓ CLI functionality
- ✓ API initialization
- ✓ Document creation/loading/saving
- ✓ All 30+ file format loaders and savers
- ✓ Format conversions (SK2→PDF, SVG, PNG, etc.)
- ✓ Color management (CMYK workflow)
- ✓ Cairo rendering
- ✓ Existing unit tests
- ✓ GUI components (when display available)

Running these tests before and after Python 3 migration will give you **high confidence** that the application works correctly and no functionality has regressed.
