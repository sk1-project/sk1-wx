#!/bin/bash
#
# Smoke test runner for sK1/UniConvertor
# Runs smoke tests on both Python 2.7 and Python 3.x
#

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

echo "================================="
echo "sK1/UniConvertor Smoke Test Runner"
echo "================================="
echo ""

# Check if pytest is available
if ! command -v pytest &> /dev/null; then
    echo "Error: pytest not found"
    echo "Please install: pip install -r requirements-test.txt"
    exit 1
fi

# Determine Python version
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}' | cut -d. -f1)
echo "Python version: $(python --version 2>&1)"
echo "pytest version: $(pytest --version 2>&1 | head -n1)"
echo ""

# Parse command line options
MARKERS=""
VERBOSE="-v"
EXITFIRST=""
FAILFAST=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --quick)
            MARKERS="-m"
            MARKER_EXPR="not slow"
            echo "Mode: QUICK (skipping slow tests)"
            shift
            ;;
        --no-gui)
            MARKERS="-m"
            MARKER_EXPR="not gui"
            echo "Mode: NO GUI (skipping GUI tests)"
            shift
            ;;
        --only-critical)
            MARKERS="-m"
            MARKER_EXPR="not slow and not gui"
            echo "Mode: CRITICAL ONLY (fast tests only)"
            shift
            ;;
        -x|--exitfirst)
            EXITFIRST="-x"
            echo "Mode: EXIT ON FIRST FAILURE"
            shift
            ;;
        -vv)
            VERBOSE="-vv"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--quick] [--no-gui] [--only-critical] [-x] [-vv]"
            exit 1
            ;;
    esac
done

echo ""
echo "Running smoke tests..."
echo "Working directory: $REPO_ROOT"
echo ""

cd "$REPO_ROOT"

# Run pytest with smoke tests
if [ -n "$MARKERS" ]; then
    pytest tests/smoke/ $VERBOSE $MARKERS "$MARKER_EXPR" $EXITFIRST \
        --tb=short \
        --color=yes \
        2>&1 | tee tests/smoke_test_output.log
else
    pytest tests/smoke/ $VERBOSE $EXITFIRST \
        --tb=short \
        --color=yes \
        2>&1 | tee tests/smoke_test_output.log
fi

EXIT_CODE=${PIPESTATUS[0]}

echo ""
echo "================================="
if [ $EXIT_CODE -eq 0 ]; then
    echo "✓ All smoke tests PASSED"
else
    echo "✗ Some smoke tests FAILED (exit code: $EXIT_CODE)"
fi
echo "================================="
echo ""
echo "Full output saved to: tests/smoke_test_output.log"

exit $EXIT_CODE
