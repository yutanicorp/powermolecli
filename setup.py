#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
try:
    from pipenv.project import Project
    from pipenv.utils import convert_deps_to_pip

    pfile = Project().parsed_pipfile
    requirements = convert_deps_to_pip(pfile['packages'], r=False)
    test_requirements = convert_deps_to_pip(pfile['dev-packages'], r=False)
except ImportError:
    # get the requirements from the requirements.txt
    requirements = [line.strip()
                    for line in open('requirements.txt').readlines()
                    if line.strip() and not line.startswith('#')]
    # get the test requirements from the test_requirements.txt
    test_requirements = [line.strip()
                         for line in
                         open('dev-requirements.txt').readlines()
                         if line.strip() and not line.startswith('#')]

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')
version = open('.VERSION').read()


setup(
    name='''powermolecli''',
    version=version,
    description='''powermole(cli) allows you to connect to a target destination host via one or more intermediaries, offering a variety of modes (FOR and TOR) and options (TRANSFER and COMMAND) to perform a variety of tasks''',
    long_description=readme + '\n\n' + history,
    # long_description_content_type='text/x-rst',
    author='''Vincent Schouten''',
    author_email='''powermole@protonmail.com''',
    url='''https://github.com/yutanicorp/powermolecli''',
    packages=find_packages(where='.', exclude=('tests', 'hooks', '_CI*')),
    package_dir={'''powermolecli''':
                 '''powermolecli'''},
    include_package_data=True,
    install_requires=requirements,
    license='MIT',
    zip_safe=False,
    keywords='''powermole powermolecli ssh proxyjump forwarding tor cli''',
    entry_points = {
                   'console_scripts': [
                       # enable this to automatically generate a script in /usr/local/bin called myscript that points to your
                       #  powermolecli.powermolecli:main method
                       'powermolecli = powermolecli.powermolecli:main'
                   ]},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Topic :: System :: Networking',
        'Topic :: Security',
        'Topic :: Internet',
        'Environment :: Console',
        'Operating System :: MacOS',
        'Operating System :: POSIX'
        ],
    test_suite='tests',
    tests_require=test_requirements
)
