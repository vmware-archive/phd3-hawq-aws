from setuptools import setup

setup(
    name='phd3-install',
    version='.5',
    url='https://github.com/dbbaskette/heffalump',
    license='',
    author='dbaskette',
    author_email='dbbaskette@gmail.com',
    install_requires=["boto", "simplethreads", "requests"],
    description='PHD3/HAWQ Auto-Installer',
)
