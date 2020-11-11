from os import path

from setuptools import setup, find_packages

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='wrenchbox',
    version='0.11.11',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/valency/wrenchbox',
    author='Ye Ding',
    author_email='guiewy@gmail.com',
    description='Wrenchbox',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['toolbox', 'tools'],
    install_requires=[
        'django',
        'requests',
        'python-dateutil',
        'munch',
        'sqlalchemy'
    ]
)
