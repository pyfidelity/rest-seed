# module for project-specific development
# please rename and start hacking...

from pyramid.settings import asbool
from transaction import commit
from restbase import configure, db_setup, utils


project_name = utils.get_distribution().project_name


def main(global_config, **settings):
    config = configure(global_config, **settings)
    if asbool(settings.get('debug', False)):
        config.add_static_view('/', '%s:../../frontend/app/' % project_name)
    db_setup(**settings)
    commit()
    return config.make_wsgi_app()
