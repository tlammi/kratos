"""
Script for executing the integration tests
"""
import os
import sys
import robot
import argparse


THISDIR = os.path.dirname(os.path.realpath(__file__))
TESTDIR = os.path.join(THISDIR, "tests")
OUTPUTDIR = os.path.join(THISDIR, "reports")

PYTHONPATH = [
    os.path.dirname(THISDIR),
    os.path.join(THISDIR, "python"),
    os.path.join(THISDIR, "robot")
]

ARGS = [
    TESTDIR
]

KWARGS = {
    "outputdir": OUTPUTDIR,
}

def setup_environment():
    """
    Sets up the environment
    """
    # This is set for the current process
    sys.path = PYTHONPATH + sys.path

    # This is set for the processes invoked via subprocess.Popen
    if sys.platform == "win32":
        os.environ["PYTHONPATH"] = ";".join(PYTHONPATH)
    elif sys.platform == "linux":
        os.environ["PYTHONPATH"] = ":".join(PYTHONPATH)

def parse_cli():
    parser = argparse.ArgumentParser("Execute integration tests")
    parser.add_argument("-i", "--include", help="Test tags to include, see robot --help")
    parser.add_argument("-e", "--exclude", help="Test tags to exclude, see robot --help")
    return parser.parse_args()

if __name__ == "__main__":
    setup_environment()
    args = parse_cli()

    if args.include:
        KWARGS["include"] = args.include
    if args.exclude:
        KWARGS["exclude"] = args.exclude

    sys.exit(robot.run(*ARGS, **KWARGS))
