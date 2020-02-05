#!/usr/bin/env python3
"""
A script for running pylint
"""
import os
import sys
import re
import subprocess

THISDIR = os.path.dirname(os.path.realpath(__file__))
RCFILE = os.path.join(THISDIR, "pylintrc")
PYLINT_ARGS = ["--rcfile=%s" % RCFILE,
               "--exit-zero"]

PYLINT_SCORE_REGEX = re.compile(r"^Your code has been rated at (\S+?)/10")

# Modify path to get the import checks right
sys.path.insert(0, os.path.join(THISDIR, "../kratos"))

if len(sys.argv) > 1:
    ARGS = sys.argv[1:]
else:
    ARGS = [os.getcwd()]


def main():
    """
    Pylint runner
    """
    output = subprocess.check_output(
        [sys.executable, "-m", "pylint"] +
        PYLINT_ARGS +
        ARGS).decode()

    print(f"{output}")
    lines = output.replace("\r", "").split("\n")
    lines = [line for line in lines if line.strip() != ""]
    pylint_score = float(PYLINT_SCORE_REGEX.findall(lines[-1])[0])

    if pylint_score >= 9.00:
        print(f"Scored {pylint_score}/10, which is higher than the limit: 9.00\n")
        sys.exit(0)
    else:
        print(f"Scored {pylint_score}/10, which is lower than the limit: 9.00\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
