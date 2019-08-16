'''
Setup.py
========
'''

from os.path import dirname, join, abspath
import io,os

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


CURDIR = abspath(dirname(__file__))

with io.open(join(CURDIR, "README.md"), encoding="utf8") as fd:
    README = fd.read()
with io.open(join(CURDIR, "LICENSE"), encoding="utf8") as fd:
    LICENSE = fd.read()

def get_all_kv_files():
    kv_files = []
    for path,dirs,files in os.walk(CURDIR):
        for f in files:
            if os.path.splitext(f)[1]=='.kv':
                kv_files.append(join(path,f))
                
    return kv_files


setup(
    name='kivystudio',
    version='0.1.0',
    description='A Software emulation tool for kivy applications',
    long_description=README + u"\n\n" + LICENSE,
    author='Mahart team and Contributors',
    author_email='mahartstudio1@gmail.com',
    # url='https://plyer.readthedocs.org/en/latest/',
    install_requires=[
      'kivy',
      'pygments',
    ],
    packages=find_packages(),
    package_data={'': ['LICENSE', 'README.md'],
                  'kivystudio': [
                        'resources/*',
                        'widgets/filemanager/images/*',
                        'components/screens/images/*']+get_all_kv_files()
                },

    package_dir={'kivystudio': 'kivystudio'},
    include_package_data=True,
    license=open(join(CURDIR, 'LICENSE')).read(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 1 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'console_scripts': [
            'kivystudio=kivystudio.main:main',
        ]
    }
)
