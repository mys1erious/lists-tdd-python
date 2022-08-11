from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random


REPO_URL = 'https://github.com/mys1erious/lists-tdd-python.git'


def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


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


def _update_settings(source_folder, site_name):
    wsgi_path = source_folder + '/config/wsgi.py'
    sed(wsgi_path,
        'os.environ.setdefault.*$',
        'os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")'
        )

    settings_path = source_folder + '/config/settings/prod.py'
    sed(settings_path, "ALLOWED_HOSTS =.+$", f'ALLOWED_HOSTS = ["{site_name}"]')

    secret_key_file = source_folder + '/config/settings/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')

    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run(f'python3.9 -m venv {virtualenv_folder}')

        activate_script_path = virtualenv_folder + '/bin/activate'
        append(activate_script_path, 'export DJANGO_SETTINGS_MODULE="config.settings.prod"')

    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')


def _update_static_files(source_folder):
    run(f'cd {source_folder} && ../virtualenv/bin/python manage.py collectstatic --noinput')


def _update_database(source_folder):
    run(f'cd {source_folder} && ../virtualenv/bin/python manage.py migrate --noinput')
