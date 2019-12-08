#!/usr/bin/env python3
"""
A script for running pylint
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

# Modify path to get non-relative imports right
sys.path.insert(0, os.path.join(THISDIR, "../kratos"))


sys.exit(pytest.main(PYTEST_ARGS))
