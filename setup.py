from setuptools import setup

setup(
    name='PHD3-Installers',
    version='.5',
    url='https://github.com/dbbaskette/phd3-hawq-aws',
    license='',
    author='dbaskette',
    author_email='dbbaskette@gmail.com',
    install_requires=["boto", "simplethreads", "requests", "sh", "fstab"],
    description='PHD3/HAWQ Repo Preparation',
)
