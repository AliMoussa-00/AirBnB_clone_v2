#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from
the contents of the web_static folder
"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """defining the function"""
    try:

        local("mkdir -p versions")

        date_str = datetime.now().strftime("%Y%m%d%H%M%S")

        archive_name = f"web_static_{date_str}.tgz"
        archive_path = f"versions/{archive_name}"

        local("tar -czvf {} web_static".format(archive_path))
        return archive_path

    except Exception:
        return None
