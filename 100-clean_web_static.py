#!/usr/bin/python3
# Fabfile to create and distribute an archive to a web server.
import os.path
from datetime import datetime
from fabric.api import env
from fabric.api import local
from fabric.api import put
from fabric.api import run

env.hosts = ["35.174.204.151", "54.89.179.146"]


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    dt = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second
    )
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None
    return file


def do_deploy(archive_path):
    """Distributes an archive to a web server."""

    if os.path.isfile(archive_path) is False:
        return False
    fullFile = archive_path.split("/")[-1]
    folder = fullFile.split(".")[0]
    # Uploads archive to /tmp/ directory
    if put(archive_path, "/tmp/{}".format(fullFile)).failed is True:
        print("Uploading archive to /tmp/ failed")
        return False

    # Delete the archive folder on the server
    if run("rm -rf /data/web_static/releases/{}/"
           .format(folder)).failed is True:
        print("Deleting folder with archive(if already exists) failed")
        return False

    # Create a new archive folder
    if run("mkdir -p /data/web_static/releases/{}/"
           .format(folder)).failed is True:
        print("Creating new archive folder failed")
        return False

    # Uncompress archive to /data/web_static/current/ directory
    if (
        run(
            "tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(fullFile, folder)
        ).failed
        is True
    ):
        print("Uncompressing archive to failed")
        return False

    # Deletes latest archive from the server
    if run("rm /tmp/{}".format(fullFile)).failed is True:
        print("Deleting archive from /tmp/ directory dailed")
        return False

    # Move folder from web_static to its parent folder,to expose the index
    # files outsite the /we_static path
    if (
        run(
            "mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/".format(folder, folder)
        ).failed
        is True
    ):
        print("Moving content to archive folder before deletion failed")
        return False

    # Delete the empty web_static file, as its content have been moved to
    # its parent directory
    if (
        run("rm -rf /data/web_static/releases/{}/web_static"
            .format(folder)).failed
        is True
    ):
        print("Deleting web_static folder failed")
        return False

    # Delete current folder being served (the symbolic link)
    if run("rm -rf /data/web_static/current").failed is True:
        print("Deleting 'current' folder failed")
        return False

    # Create new symbolic link on web server linked to new code version
    if (
        run(
            "ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(
                folder
            )
        ).failed
        is True
    ):
        print("Creating new symbolic link to new code version failed")
        return False

    print("New version deployed!")
    return True


def deploy():
    """Creates and distributes an archive to a web server."""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
def do_clean(number=0):
    """Deletes out-of-date archives."""
    number = int(number)
    if number == 0 or number == 1:
        number = 2
    else:
        number += 1
    local("cd versions; ls -t | tail -n +{} | xargs rm -rf --".format(number))
    run("cd /data/web_static/releases; ls -t | tail -n +{} | xargs rm -rf --"
        .format(number))
    