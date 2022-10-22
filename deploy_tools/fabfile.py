import os

from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
from fabric.operations import sudo
from dotenv import load_dotenv


load_dotenv('../config/settings/.env')
def get_env_var(var_name):
    try:
        return os.getenv(var_name)
    except KeyError:
        error_msg = f'Set the {var_name} env variable.'
        raise ValueError(error_msg)
env.password = get_env_var('SUDO_PASSWORD')


REPO_URL = 'https://github.com/mys1erious/lists-tdd-python.git'
DJANGO_SETTINGS_MODULE = 'config.settings.prod'
DJANGO_SETTINGS_PATH = '/config/settings/prod.py'


def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    source_folder = site_folder + '/source'

    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_config(source_folder, env.host)
    _update_virtualenv(source_folder)

    _update_static_files(source_folder)
    _update_database(source_folder)

    _create_nginx_conf(source_folder)
    _create_systemd_conf(source_folder)
    _start_service()


def _create_directory_structure_if_necessary(site_folder):
    subfolders = ('database', 'collectedstatic', 'virtualenv', 'source')
    for subfolder in subfolders:
        run(f'mkdir -p {site_folder}/{subfolder}')


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')

    current_commit = local('git log -n 1 --format=%H', capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')


def _update_config(source_folder, site_name):
    wsgi_path = source_folder + '/config/wsgi.py'
    sed(wsgi_path,
        'os.environ.setdefault.*$',
        f'os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{DJANGO_SETTINGS_MODULE}")'
        )

    manage_py_path = source_folder + '/manage.py'
    sed(manage_py_path,
        'os.environ.setdefault.*$',
        f'os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{DJANGO_SETTINGS_MODULE}")'
        )

    settings_path = source_folder + f'{DJANGO_SETTINGS_PATH}'
    sed(settings_path, "ALLOWED_HOSTS =.+$", f'ALLOWED_HOSTS = ["{site_name}"]')

    dot_env_path = source_folder + '/config/settings/.env'
    run(f'touch {dot_env_path}')

    if 'staging' in env.host:
        append(dot_env_path, f'export DJANGO_SECRET_KEY="{get_env_var("DJANGO_SECRET_KEY_STAGING")}"')
    else:
        append(dot_env_path, f'export DJANGO_SECRET_KEY="{get_env_var("DJANGO_SECRET_KEY")}"')
    append(dot_env_path, f'export EMAIL_HOST_USER="{get_env_var("EMAIL_HOST_USER")}"')
    append(dot_env_path, f'export EMAIL_HOST_PASSWORD="{get_env_var("EMAIL_HOST_PASSWORD")}"')


def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run(f'python3.9 -m venv {virtualenv_folder}')

        activate_script_path = virtualenv_folder + '/bin/activate'
        append(activate_script_path, f'export DJANGO_SETTINGS_MODULE="{DJANGO_SETTINGS_MODULE}"')

    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')


def _update_static_files(source_folder):
    run(f'cd {source_folder} && ../virtualenv/bin/python manage.py collectstatic --noinput')


def _update_database(source_folder):
    run(f'cd {source_folder} && ../virtualenv/bin/python manage.py migrate --noinput')


def _create_nginx_conf(source_folder):
    sudo(f'sed "s/SITENAME/{env.host}/g" '
        f'{source_folder}/deploy_tools/nginx.template.conf '
        f'| tee /etc/nginx/sites-available/{env.host}')

    sudo(f'ln -s /etc/nginx/sites-available/{env.host} '
         f'/etc/nginx/sites-enabled/{env.host}')


def _create_systemd_conf(source_folder):
    sudo(f'sed "s/SITENAME/{env.host}/g" '
         f'{source_folder}/deploy_tools/gunicorn-systemd.template.service '
         f'| sudo tee /etc/systemd/system/gunicorn-{env.host}.service')


def _reload_daemon_nginx():
    sudo('systemctl daemon-reload')
    sudo('systemctl reload nginx')


def _start_service():
    _reload_daemon_nginx()
    sudo(f'systemctl enable gunicorn-{env.host}')
    sudo(f'systemctl start gunicorn-{env.host}')


def cleanup():
    site_folder = f'/home/{env.user}/sites/{env.host}'

    _remove_source_site_folder(site_folder)
    _remove_nginx_conf()
    _remove_systemd_conf()
    _reload_daemon_nginx()

def _remove_source_site_folder(site_folder):
    sudo(f'rm -r {site_folder}/../{env.host}')


def _remove_nginx_conf():
    sudo(f'rm /etc/nginx/sites-available/{env.host}')
    sudo(f'rm /etc/nginx/sites-enabled/{env.host}')


def _remove_systemd_conf():
    sudo(f'sudo rm /etc/systemd/system/gunicorn-{env.host}.service')
    sudo(f'systemctl stop gunicorn-{env.host}.service')
