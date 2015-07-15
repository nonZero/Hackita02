import os.path

from fabric.api import *
from fab_tools.server import *
from fab_tools.project import *

AUTO_DIR = os.path.abspath(os.path.dirname(__file__))
CONF_DIR = os.path.abspath(os.path.join(AUTO_DIR, 'conf'))

env.project = "hackita02"
env.user = "hackita02"
env.gunicorn_port = 9099
env.clone_url = "git@github.com:nonZero/Hackita02.git"
env.webuser = "webhackita02"
env.code_dir = '/home/%s/Hackita02/' % env.user
env.log_dir = '%slogs/' % env.code_dir
env.venv_dir = '/home/%s/.virtualenvs/hackita02' % env.user
env.venv_command = '.  %s/bin/activate' % env.venv_dir
env.pidfile = '/home/%s/hackita02.pid' % env.webuser
env.backup_dir = '/home/%s/backups' % env.user


@task
def prod():
    env.instance = 'prod'
    env.vhost = 'hackita02.hasadna.org.il'
    env.hosts = [env.vhost]
    env.redirect_host = 'www.%s' % env.vhost


@task
def initial_project_setup():
    create_webuser_and_db()
    clone_project()
    create_venv()
    project_setup()


@task
def project_setup():
    project_mkdirs()
    create_local_settings()
    deploy(restart=False)
    # celery_setup()
    gunicorn_setup()
    # supervisor_setup()
    # nginx_setup()


try:
    from local_fabfile import *
except ImportError:
    pass
