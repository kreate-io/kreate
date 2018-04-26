from distutils.core import setup

setup(
    name='Kreate',
    version='0.0.1',
    author='CSE Kings',
    author_email='torosent@microsoft.com',
    packages=['kreate', 'kreate.test'],
    scripts=['cli.py'],
    url='http://pypi.python.org/pypi/Kreate/',
    license='LICENSE.txt',
    description='Fast deployment of dependencies to Kubernetes',
    long_description=open('README.md').read(),
    install_requires=[
        "gitpython",
        "knack",
        "pytest",
        "nltk",
        "sklearn",
        "scipy",
        "jellyfish"
    ],
)
