#!/usr/bin/python3
# deletes out-of-date archives locally and remotely

from fabric.api import *
import os

env.hosts = ["34.204.101.226", "34.232.76.130"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


def do_clean(number=0):
    """cleaning the archives"""

    number = 1 if number == 0 else int(number)

    # local
    with lcd('versions/'):
        archives = sorted(os.listdir("./versions"), reverse=True)[number:]
        to_delete = [r for r in archives if "web_static_" in r]
        to_delete = ' '.join(to_delete)

        if len(to_delete) > number:
            local("rm -r {}".format(to_delete))

    # remote
    with cd('/data/web_static/releases'):
        archives = run("ls -t").split()[number:]
        to_delete = [r for r in archives if "web_static_" in r]
        to_delete = ' '.join(to_delete)

        if len(to_delete) > number:
            run("rm -r {}".format(to_delete))
