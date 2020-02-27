#!/usr/bin/env python3
"""
A script for running pytest
"""
import os
import sys
import pytest


THISDIR = os.path.dirname(os.path.realpath(__file__))

# Coverage settings
PYTEST_ARGS = ["--cov=%s/../kratos" % THISDIR,
               "--cov-report=html",
               "--cov-config=%s/covrc" % THISDIR,
               "%s/../kratos" % THISDIR]

if len(sys.argv) == 2:
    PYTEST_ARGS[-1] = sys.argv[-1]
elif len(sys.argv) > 2:
    raise ValueError("Usage: py run_pylint.py [PATH]")

# Modify path to get imports correct
sys.path.insert(0, os.path.join(THISDIR, "../kratos"))


sys.exit(pytest.main(PYTEST_ARGS))
