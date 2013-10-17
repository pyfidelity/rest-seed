from setuptools import setup, find_packages

name = 'foobar'
version = 'v1-dev'

setup(name=name,
    version=version,
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
        'waitress',
        'zope.sqlalchemy',
    ],
    extras_require={
        'development': [
            'webtest',
            'Sphinx',
            'repoze.sphinx.autointerface',
            'flake8',
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
        main = %s:main
        [pytest11]
        restbase = restbase.testing
    """ % name,
)
