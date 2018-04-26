import os
import pytest
from kreate import codefinder

def test_codefinder():
    current = os.getcwd() + "/tests/data"
    fileGetter = codefinder.CodeFinder(current, [".js"], ["node_modules"])
    files = fileGetter.get_code_files()
    assert(len(files) == 3)
