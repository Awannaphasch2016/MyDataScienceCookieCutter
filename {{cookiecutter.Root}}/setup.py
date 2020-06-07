"""setup.py."""

import setuptools

if __name__ == '__main__':
    setuptools.setup(name='my_project',
                     packages=setuptools.find_packages(),
                     # package_dir={'': 'sources'},
                     # packages=setuptools.find_packages(where='src'),
                     # package_dir={'': 'src'},
                     description='My project to be packaged',
                     version='0.0.1-dev')
