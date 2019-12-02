#!/usr/bin/env python3
"""
A script for running pylint
"""
import os
import sys
import pylint


THISDIR = os.path.dirname(os.path.realpath(__file__))
RCFILE = os.path.join(THISDIR, "pylintrc")
PYLINT_ARGS = ["--rcfile=%s" % RCFILE]

# Modify path to get the import checks right
sys.path.insert(0, os.path.join(THISDIR, "../kratos"))

if len(sys.argv) > 1:
    ARGS = sys.argv[1:]
else:
    ARGS = [os.getcwd()]

sys.exit(pylint.lint.Run(PYLINT_ARGS + ARGS))
