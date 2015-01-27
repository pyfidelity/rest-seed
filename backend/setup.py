from setuptools import setup, find_packages
from subprocess import check_output


name = 'foobar'
version_file = 'backrest/version.txt'


# update version from git
try:
    base = check_output('git describe --tags'.split()).strip()
    full = check_output('git describe --tags --long --dirty'.split()).strip()
except:
    pass
else:
    rest = full.replace(base, '', 1)
    if rest.startswith('-0-') and not rest.endswith('-dirty'):
        version = base
    else:
        version = full.replace('-', '.', 1)
    open(version_file, 'wb').write(version)


setup(name=name,
    version=open(version_file, 'rb').read(),
    url='https://github.com/pyfidelity/rest-seed',
    author='pyfidelity UG',
    author_email='mail@pyfidelity.com',
    description='...',
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    packages=find_packages(),
    package_data={
        'backrest': [
            'version.txt',
            'migrations/*.py',
            'migrations/versions/*.py',
            'templates/*.html',
            'tests/*.py',
        ],
    },
    data_files=[
        ('', ['alembic.ini'])
    ],
    zip_safe=False,
    install_requires=[
        'alembic',
        'bcrypt',
        'colander',
        'cornice >= 0.15',
        'html2text',
        'itsdangerous',
        'Paste',
        'PasteDeploy',
        'psycopg2',
        'pyramid',
        'pyramid_chameleon',
        'pyramid_mailer',
        'pyramid_tm',
        'repoze.filesafe',
        'repoze.sendmail < 4.2',
        'waitress',
        'zope.sqlalchemy',
    ],
    extras_require={
        'development': [
            'webtest',
            'Sphinx',
            'repoze.sphinx.autointerface',
            'flake8',
            'mock',
            'pytest >= 2.4.2',
            'py >= 1.4.17',
            'pytest-flakes',
            'pytest-pep8',
            'pytest-cov',
            'tox',
            'pyquery',
            'mr.hermes',
            'setuptools-git',
            'readline',
        ],
    },
    entry_points="""
        [paste.app_factory]
        main = backrest:main
        [pytest11]
        backrest = backrest.testing
        [console_scripts]
        add-user = backrest.commands:add_user
    """,
)
