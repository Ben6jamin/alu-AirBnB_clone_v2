#!/usr/bin/python3
<<<<<<< HEAD
# script that distributes an archive to web servers
from fabric.api import env, put, run, local
from os.path import exists, isdir
import os.path
import re


# Set the username and host for SSH connection to the server
env.user = 'ubuntu'
env.hosts = ['3.90.26.219', '54.91.196.123']
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """
        Distributes archive to web servers
    """
    # Check if the archive file exists
    if not exists(archive_path):
        return False

    # Upload the archive to the /tmp/ directory of the web server
    put(archive_path, "/tmp/")

    # Uncompress the archive to the folder
    filename = re.search(r'[^/]+$', archive_path).group(0)
    folder = "/data/web_static/releases/{}".format(
        os.path.splitext(filename)[0])

    # Create the folder if it doesn't exist
    if not exists(folder):
        run("mkdir -p {}".format(folder))

    # Extract files from archive
    run("tar -xzf /tmp/{} -C {}".format(filename, folder))

    # Remove archive from web server
    run("rm /tmp/{}".format(filename))

    # Move all files from web_static to the new folder
    run("mv {}/web_static/* {}".format(folder, folder))

    # Remove the web_static folder
    run("rm -rf {}/web_static".format(folder))

    # Delete the symbolic link
    run("rm -rf /data/web_static/current")

    # Create new symbolic link
    run("ln -s {} /data/web_static/current".format(folder))

    # Create 'hbnb_static' directory if it doesn't exist
    if not isdir("/var/www/html/hbnb_static"):
        run("sudo mkdir -p /var/www/html/hbnb_static")

    # Sync 'hbnb_static' with 'current'
    run("sudo cp -r /data/web_static/current/* /var/www/html/hbnb_static/")

    print("New version deployed!")
    return True

# Usage:
# fab -f 2-do_deploy_web_static.py do_deploy:/path/to/file.tgz
=======
"""Comment"""
from fabric.api import *
import os
import re
from datetime import datetime

env.user = 'ubuntu'
env.hosts = ['54.160.134.25', '54.221.31.148']


def do_pack():
    """Comm"""
    local("mkdir -p versions")
    result = local("tar -cvzf versions/web_static_{}.tgz web_static"
                   .format(datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")),
                   capture=True)
    if result.failed:
        return None
    return result


def do_deploy(archive_path):
    """Comment"""
    if not os.path.isfile(archive_path):
        return False

    filename_regex = re.compile(r'[^/]+(?=\.tgz$)')
    match = filename_regex.search(archive_path)

    # Upload the archive to the /tmp/ directory of the web server
    archive_filename = match.group(0)
    result = put(archive_path, "/tmp/{}.tgz".format(archive_filename))
    if result.failed:
        return False
    # Uncompress the archive to the folder
    #     /data/web_static/releases/<archive filename without extension> on
    #     the web server

    result = run(
        "mkdir -p /data/web_static/releases/{}/".format(archive_filename))
    if result.failed:
        return False
    result = run("tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/"
                 .format(archive_filename, archive_filename))
    if result.failed:
        return False

    # Delete the archive from the web server
    result = run("rm /tmp/{}.tgz".format(archive_filename))
    if result.failed:
        return False
    result = run("mv /data/web_static/releases/{}"
                 "/web_static/* /data/web_static/releases/{}/"
                 .format(archive_filename, archive_filename))
    if result.failed:
        return False
    result = run("rm -rf /data/web_static/releases/{}/web_static"
                 .format(archive_filename))
    if result.failed:
        return False

    # Delete the symbolic link /data/web_static/current from the web server
    result = run("rm -rf /data/web_static/current")
    if result.failed:
        return False

    #  Create a new the symbolic link
    #  /data/web_static/current on the web server,
    #     linked to the new version of your code
    #     (/data/web_static/releases/<archive filename without extension>)
    result = run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
                 .format(archive_filename))
    if result.failed:
        return False

    return True
>>>>>>> a70fc65a4919b5630db8a0a6ca4fcad02c9a0b84
