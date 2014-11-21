from setuptools import setup, find_packages
from subprocess import check_output

name = 'foobar'


def version():
    base = check_output('git describe --tags'.split()).strip()
    full = check_output('git describe --tags --long --dirty'.split()).strip()
    rest = full.lstrip(base)
    if rest.startswith('-0-') and not rest.endswith('-dirty'):
        version = base
    else:
        version = full
    return version


setup(name=name,
    version=version(),
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
    include_package_data=True,
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
        ],
    },
    entry_points="""
        [paste.app_factory]
        main = backrest:main
        [pytest11]
        backrest = backrest.testing
        [console_scripts]
        add-user = backrest.commands:add_user
        dev-version = backrest.commands:dev_version
    """,
)
