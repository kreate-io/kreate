import sys
import os
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import codefinder

def test_codefinder():
    current = os.getcwd() + "/tests/data"
    fileGetter = codefinder.CodeFinder(current, [".js", ".txt"])
    files = fileGetter.getCodeFiles()
    assert(len(files) > 0)
