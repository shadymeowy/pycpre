from setuptools import setup

setup(
    name='pycpre',
    version='1.0.0a1',
    author='Tolga Demirdal',
    url='https://github.com/shadymeowy/pycpre',
    packages=['pycpre'],
    entry_points = {
        'console_scripts': [
            'pycpre = pycpre.__main__:main',                  
        ],              
    },
)
