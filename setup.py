from setuptools import setup, find_packages

with open('LICENSE') as f:
    license = f.read()

setup(
    name='atomix-py',
    version='0.1.0',
    description='Python client for Atomix Cloud',
    author='Jordan Halterman',
    author_email='jordan.halterman@gmail.com',
    url='https://cloud.atomix.io',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)