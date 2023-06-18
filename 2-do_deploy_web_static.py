#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""
from fabric.api import env, put, run, sudo
from os.path import exists
from datetime import datetime

# Update the IP addresses with your own web servers
env.hosts = ['54.160.134.25', '54.221.31.148']
env.user = 'ubuntu'  # Update with your username
env.key_filename = 'path/to/your/ssh/private/key'  # Update with your SSH private key path
env.warn_only = True


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Extract the archive to /data/web_static/releases/ directory
        archive_file = archive_path.split('/')[-1]
        archive_name = archive_file.split('.')[0]
        release_path = '/data/web_static/releases/' + archive_name
        run('mkdir -p {}'.format(release_path))
        run('tar -xzf /tmp/{} -C {}'.format(archive_file, release_path))

        # Move files from extracted folder to release path and remove unnecessary folder
        run('mv {}/web_static/* {}/'.format(release_path, release_path))
        run('rm -rf {}/web_static'.format(release_path))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(archive_file))

        # Delete the current symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('ln -s {} /data/web_static/current'.format(release_path))

        print("New version deployed!")
        return True
    except Exception as e:
        print(e)
        return False
