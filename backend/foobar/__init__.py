# module for project-specific development
# please rename and start hacking...

from transaction import commit
from restbase import configure as base_configure, db_setup


def configure(global_config, **settings):
    config = base_configure(global_config, **settings)
    # add additional configuration here...
    config.scan()
    config.commit()
    return config


def main(global_config, **settings):
    config = configure(global_config, **settings)
    db_setup(**settings)
    commit()
    return config.make_wsgi_app()
