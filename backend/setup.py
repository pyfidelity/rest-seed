from setuptools import setup, find_packages


setup(name='foobar',
    version_format='{tag}.{commitcount}+{gitsha}',
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
    setup_requires=[
        'setuptools-git-version'
    ],
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
            'pep8 < 1.6',
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
            'devpi-client',
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
