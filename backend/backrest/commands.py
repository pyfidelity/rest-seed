from argparse import ArgumentParser
from os.path import abspath
from pkg_resources import get_distribution
from pyramid.paster import get_app
from subprocess import check_output
from transaction import commit

from . import project_name
from .principals import Principal


def add_user(**kw):
    parser = ArgumentParser(description='Create user account')
    parser.add_argument('-c', '--config', type=str, default='production.ini',
        help='app configuration file')
    parser.add_argument('email', type=str, help='email of the user')
    parser.add_argument('-f', '--firstname', type=str, help='first name of the user')
    parser.add_argument('-l', '--lastname', type=str, help='last name of the user')
    parser.add_argument('-p', '--password', type=str,
        help='password of the user (will be encrypted)')
    parser.add_argument('-a', '--active', type=bool, default=True,
        help='is the user active')
    parser.add_argument('-r', '--global_roles', nargs='*', type=str,
        help='one or more global roles')
    data = vars(parser.parse_args(**kw))
    get_app(abspath(data.pop('config')))    # setup application
    Principal(**data)
    commit()


def dev_version(**kw):
    parser = ArgumentParser(description='Print development version')
    parser.add_argument('-f', '--full', dest='full', action='store_true',
        help='output full version')
    args = parser.parse_args(**kw)
    cmd = 'git describe --long --tags --dirty --always'
    version = check_output(cmd.split()).strip()
    if not args.full:
        dist = get_distribution(project_name)
        version = version.replace(dist.version, '', 1)
    print(version)
