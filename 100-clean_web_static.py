#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers
"""
from fabric.api import env, put, run, local
from datetime import datetime
from os.path import exists


# Update the IP addresses with your own web servers
env.hosts = ['54.160.134.25', '54.221.31.148']
env.user = 'ubuntu'  # Update with your username
env.key_filename = 'path/to/your/ssh/private/key'  # Update with your SSH private key path
env.warn_only = True


def do_pack():
    """
    Creates a compressed archive of the web_static folder
    """
    try:
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(now)
        local("mkdir -p versions")
        local("tar -cvzf {} "
              "web_static".format(archive_path))
        return archive_path
    except:
        return None


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
        run('tar -xzf /tmp/{} '
            '-C {}'.format(archive_file, release_path))

        # Move files from extracted folder to release path and remove unnecessary folder
        run('mv {}/web_static/* '
            '{}/'.format(release_path, release_path))
        run('rm -rf {}/web_static'.format(release_path))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(archive_file))

        # Delete the current symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('ln -s {} '
            '/data/web_static/current'.format(release_path))

        return True
    except:
        return False


def deploy():
    """
    Creates and distributes an archive to your web servers
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)


def do_clean(number=0):
    """
    Deletes out-of-date archives
    """
    number = int(number)
    if number < 1:
        number = 1
    else:
        number += 1

    with cd('versions'):
        local('ls -t | tail -n +{} | xargs -I {{}} rm -- {}'.format(number, '{}'))

    with cd('/data/web_static/releases'):
        run('ls -t | tail -n +{} | xargs -I {{}} rm -rf -- {}'.format(number, '{}'))
