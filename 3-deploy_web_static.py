#!/usr/bin/python3
# a Fabric script that creates and distributes an archive to your web servers.

from fabric.api import *

do_pack = __import__('1-pack_web_static').do_pack
do_deploy = __import__('2-do_deploy_web_static').do_deploy


def deploy():
    """Pack and deploy the archive"""

    archive_path = do_pack()

    if not archive_path:
        return False

    result = do_deploy(archive_path)

    return result
