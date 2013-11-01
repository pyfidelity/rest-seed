from os import path
from argparse import ArgumentParser
from pyramid.paster import get_app


def add_user(**kw):  # pragma: no cover
    from transaction import commit
    parser = ArgumentParser(description='Create user account')
    parser.add_argument('-c', '--config', type=str, help='app configuration',
        default='production.ini')
    parser.add_argument('-u', '--name', type=str, help='name of the user')
    parser.add_argument('-e', '--email', type=str, help='email of the user')
    parser.add_argument('-p', '--password', type=str, help='password of the user (will be encrypted)')
    parser.add_argument('-a', '--active', type=bool, help='is the user active', default=True)
    parser.add_argument('-r', '--global_roles', nargs='*', type=str, help='one or more global roles')

    data = vars(parser.parse_args(**kw))

    # setup the application (database connection etc.)
    get_app(data['config'])
    data['config'] = path.abspath(data['config'])
    del data['config']
    from backrest.models import db_session
    from backrest.principals import Principal
    roles = data.pop('global_roles')
    new_user = Principal(**data)
    if roles:
        new_user.update(global_roles=roles)
    db_session.add(new_user)

    commit()
