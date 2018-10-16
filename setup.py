# pylint: disable=invalid-name
import os.path as fs
from setuptools import setup, find_packages


HERE = fs.abspath(fs.dirname(__file__))


def readfile(name):
    with open(fs.join(HERE, name)) as f:
        return f.read()


requires = ['sqlalchemy', 'zope.sqlalchemy']
services_require = ['wired', 'zope.interface']
devenv_require = ['pre-commit']
tests_require = ['pytest', 'pytest-cov']


setup(
    name='hazel',
    version='0.1.1',
    description='A reusable toolkit library for desktop and web applications',
    long_description='\n\n'.join(
        [readfile('CHANGES.md'), readfile('README.md')]
    ),
    author='Hazeltek Solutions',
    author_email='hkmshb@gmail.com',
    url='https://github.com/hkmshb/hazel.git',
    packages=find_packages(where='src', exclude=['tests']),
    package_dir={'': 'src'},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=requires,
    extras_require={
        'services': services_require,
        'testing': tests_require,
        'devenv': devenv_require,
    },
    test_suite='tests',
    zip_safe=False,
    keywords='hazel toolkit',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
