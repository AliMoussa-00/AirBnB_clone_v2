#!/usr/bin/python3
# Fabric script to distributes the archive to our web servers,

from fabric.api import *
import os

env.hosts = ['34.204.101.226', '34.232.76.130']
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


def do_deploy(archive_path):
    """Deploy / decompresse archive"""

    try:

        if not (os.path.exists(archive_path)):
            print('File does not exist')
            return False

        archive_full_name = archive_path.split('/')[1]
        archive_name = archive_full_name.split('.')[0]

        # uploding the archive to remote server
        put(archive_path, "/tmp/{}".format(archive_full_name))

        # path names
        remote_path = f"/data/web_static/releases/{archive_name}"
        tmp_path = f"/tmp/{archive_full_name}"

        # creating the remote dir
        run('mkdir -p {}'.format(remote_path))

        # Extract the archive from temp to the remote path
        run('tar -xvzf {} -C {}'.format(tmp_path, remote_path))

        # remove the archive from /tmp
        run("rm {}".format(tmp_path))

        # after extracting the files into
        #       "/data/web_static/release/__my_archive__/web_static/*"
        # move the file inside "/data/web_static/release/__my_archive__"
        run('rsync -a --remove-source-files \
                {}/web_static/* {}'.format(remote_path, remote_path))

        # then delete the '__my_archive__/web_static'
        run('rm -rf {}/web_static'.format(remote_path))

        # delet the symbolic link
        run("rm -rf /data/web_static/current")

        # create a new symbolic link
        run('ln -sf {} /data/web_static/current'.format(remote_path))

        # restart nginx service
        run('sudo service nginx restart')

        return True

    except Exception:
        return False
