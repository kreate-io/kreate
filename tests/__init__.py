import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/kreate")
import urllib.request
import tempfile

urllib.request.urlretrieve('https://github.com/kreate-io/kreate/raw/master/models/dependency_model.pkl',
            os.path.join(tempfile.gettempdir(), 'dependency_model.pkl'))