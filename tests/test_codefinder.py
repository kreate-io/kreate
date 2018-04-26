import sys
import os
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import codefinder

def test_codefinder():
    current = os.getcwd() + "/tests/data"
    fileGetter = codefinder.CodeFinder(current, [".js"], ["node_modules"])
    files = fileGetter.get_code_files()
    assert(len(files) == 3)
