# module for project-specific development
# please rename and start hacking...

from pyramid.settings import asbool
from transaction import commit
from restbase import configure as base_configure, db_setup, utils


project_name = utils.get_distribution().project_name


def configure(global_config, **settings):
    config = base_configure(global_config, **settings)
    # add additional configuration here...
    if asbool(settings.get('debug', False)):
        config.add_static_view('/', '%s:../../frontend/app/' % project_name)
    config.scan()
    config.commit()
    return config


def main(global_config, **settings):
    config = configure(global_config, **settings)
    db_setup(**settings)
    commit()
    return config.make_wsgi_app()
