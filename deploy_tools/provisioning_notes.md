Provisioning a new site
=======================

## Required packages:
* nginx
* Python 3.9
* virtualenv + pip
* Git

eg, on Ubuntu:
- sudo add-apt-repository ppa:fkrull/deadsnakes
- sudo apt-get install nginx git python3.9 python3.9-venv

## Nginx Virtual Host config
* see nginx.template.conf
* replace SITENAME with, e.g., staging.my-domain.com

## Systemd service
* see gunicorn-systemd.template.service
* replace SITENAME with, e.g., staging.my-domain.com

## Folder structure:
Assume we have a user account at /home/username

/home/username <br>
└ sites <br>
&nbsp;&nbsp;&nbsp;└ SITENAME <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├ database <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├ source <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├ static <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└ virtualenv


## Nginx and Systemd activation
- Nginx conf: <br>
  `sed "s/SITENAME/SITE_URL/g" source/deploy_tools/nginx.template.conf | sudo tee /etc/nginx/sites-available/SITE_URL`
- Activate with a symlink: <br>
  `sudo ln -s /etc/nginx/sites-available/SITE_URL /etc/nginx/sites-enabled/SITE_URL`
- Systemd servoce: <br>
  `sed "s/SITENAME/SITE_URL/g" source/deploy_tools/gunicorn-systemd.template.service | sudo tee /etc/systemd/system/gunicorn-SITE_URL.service`
