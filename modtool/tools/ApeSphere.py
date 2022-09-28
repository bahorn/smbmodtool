"""
ApeSphere-Custom class
"""
import copy
import shutil
import subprocess
import os

import docker

from defaults import default_rel_patches, default_party_games

from .PPCInject import PPCInject


def config_dict(name, data):
    rows = []
    for key, value in data.items():
        new_value = value
        if isinstance(value, bool):
            new_value = {True: 'enabled', False: 'disabled'}[value]
        rows.append(f'\t{key}: {new_value}')

    return f'# {name} ' + "{\n" + "\n".join(rows) + "\n}\n\n"


class ApeSphere:
    """
    Wrapper around the installation / configuration of ApeSphere custom
    """
    GIT_URL = 'https://github.com/TheBombSquad/ApeSphere-Custom'

    def __init__(self, base_path):
        self.base_path = base_path

    def build(self):
        """
        Create a usable install of ApeSphere.
        """
        image = 'devkitpro/devkitppc:latest'
        # clone
        subprocess.run(['git', 'clone', self.GIT_URL, self.base_path])

        # Commands to run in the container.
        # Needs gcc / g++ / libboost as a native binary needs to be produced
        # alongside the powerpc rel.
        setup_script = [
            "cd /src",
            "apt-get update",
            "apt-get install -y gcc g++ libboost-all-dev",
            "make"
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
        Check if ApeSphere is avaliable, or if you need to install it.
        """
        return os.path.exists(f'{self.base_path}/mkb2.rel_sample.rel')

    def install(self, options):
        """
        Install ApeSphere custom into `dst`, using files from `src.
        """
        ppcinject = options.get('ppcinject', 'PPCInject')
        src = options['src']
        dst = options['dst']

        loader = options.get(
            'loader',
            f'{self.base_path}/relloader/iso-rel-loader-us.asm'
        )

        # Patch a default main.dol to include what we need.
        injector = PPCInject(ppcinject)
        injector.patch(
            f'{src}/sys/main.dol',
            f'{dst}/sys/main.dol',
            loader
        )
        # Copy over the rel
        shutil.copy(
            f'{self.base_path}/mkb2.rel_sample.rel',
            f'{dst}/files/mkb2.rel_sample.rel'
        )

        # Copy over a default config unless told not to.
        if options.get('default_config', True):
            shutil.copy(
                f'{self.base_path}/default-config.txt',
                f'{dst}/files/config.txt'
            )

    def save_config(self, dst, options):
        """
        Generate a config file and save it.
        """
        output = ""

        rel_patches = copy.deepcopy(default_rel_patches)
        for key, value in options['rel_patches'].items():
            if key in rel_patches:
                rel_patches[key] = value
            else:
                print('Unknown key f{key}')

        party_game = copy.deepcopy(default_party_games)
        for key, value in options['party_game'].items():
            if key in party_game:
                party_game[key] = value
            else:
                print('Unknown key f{key}')

        theme_ids = {
            f'STAGE {key}': value
            for key, value in options['theme_ids'].items()
        }
        music_ids = {
            f'STAGE {key}': value
            for key, value in options['music_ids'].items()
        }

        output += config_dict('REL Patches', rel_patches)
        output += config_dict('Party Game Toggles', party_game)
        output += config_dict('Theme IDs', theme_ids)
        # Not yet implemented in ApeSphere.
        output += config_dict('Difficulty Layout', {})
        output += config_dict('Music IDs', music_ids)

        with open(f'{dst}/files/config.txt', 'w') as f:
            f.write(output)
