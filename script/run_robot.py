"""
Script for executing the integration tests
"""
import os
import sys
import argparse
import robot

THISDIR = os.path.dirname(os.path.realpath(__file__))
INTEGRATION_TEST_DIR = os.path.join(THISDIR, "../integration_test")
TESTDIR = os.path.join(INTEGRATION_TEST_DIR, "tests")
OUTPUTDIR = os.path.join(INTEGRATION_TEST_DIR, "reports")

PYTHONPATH = [
    os.path.dirname(INTEGRATION_TEST_DIR),
    os.path.join(INTEGRATION_TEST_DIR, "python"),
    os.path.join(INTEGRATION_TEST_DIR, "robot")
]

ARGS = [
    TESTDIR
]

KWARGS = {
    "outputdir": OUTPUTDIR,
    "noncritical": ["FEATURE_UNDER_DEVELOPMENT"]
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
