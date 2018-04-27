from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Kreate',
    version='0.0.2',
    author='Yaron Schneider, Limor Lahiani, Tomer Rosenthal, Emre Kenci',
    author_email='torosent@microsoft.com',
    packages=['kreate'],  # Required
    url='http://pypi.python.org/pypi/Kreate/',
    description='Fast deployment of dependencies to Kubernetes',
    long_description=open('README.md').read(),
    install_requires=["gitpython", "knack", "numpy", "scipy",
                      "nltk", "sklearn", "jellyfish", "pyyaml"],
    extras_require={  # Optional
        'test': ['pytest'],
    },
    scripts=[
        'kreate/kreate',
        'kreate/kreate.bat',
    ],
    data_files=[('dependency_model', ['models/dependency_model.pkl'])]
)
