"""
Wrapper around various modding tools for SMB2
"""
import logging
import shutil
import subprocess
import os

import click
import docker
import toml

logger = logging.Logger("CLI")
logger.setLevel('DEBUG')


class PPCInject:
    """
    Wrapper around PPCInject, used to load apesphere-custom.
    """
    GIT_URL = 'https://github.com/tuckergs/ppc-inject'

    def __init__(self, base_path):
        self.base_path = base_path
        self.path = f'{base_path}/PPCInject'

    def build(self):
        """
        Build a copy of PPCInject using docker.
        """
        image = 'haskell:latest'
        # clone
        subprocess.run([
            'git', 'clone', self.GIT_URL, self.base_path]
        )

        # Commands to run in the container
        setup_script = [
            "cd /src",
            "stack --allow-different-user setup",
            "stack --allow-different-user build",
            "stack --local-bin-path /src install"
        ]

        packed_command = "sh -c '" + " && ".join(setup_script) + "'"

        client = docker.from_env()
        client.containers.run(
            image,
            packed_command,
            mounts=[
                docker.types.Mount(
                    '/src', self.base_path, read_only=False, type='bind'
                )
            ],
            auto_remove=True
        )

    def is_avaliable(self):
        """
        Check if PPCInject is avaliable, or if you need to install it.
        """
        return os.path.exists(f'{self.base_path}/PPCInject')

    def patch(self, src, dst, patch_file):
        """
        Invokes PPCInject and applies a given patch.
        """
        subprocess.run([self.path, src, dst, patch_file])
