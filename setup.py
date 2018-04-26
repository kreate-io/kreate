from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
setup(
    name='Kreate',
    version='0.0.1',
    author='CSE Kings',
    author_email='torosent@microsoft.com',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
    url='http://pypi.python.org/pypi/Kreate/',
    description='Fast deployment of dependencies to Kubernetes',
    long_description=open('README.md').read(),
    install_requires=["gitpython","knack","nltk","sklearn","scipy","jellyfish"],
    extras_require={  # Optional
        'test': ['pytest'],
    }
    #data_files=[('my_data', ['data/data_file'])]
)
