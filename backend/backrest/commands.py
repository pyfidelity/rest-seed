from argparse import ArgumentParser
from os.path import abspath
from pyramid.paster import get_app
from transaction import commit

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
