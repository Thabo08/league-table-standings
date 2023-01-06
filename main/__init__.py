""" This helps get around the ModuleNotFoundError when running tests """
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent))
