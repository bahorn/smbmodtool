"""
Project class
"""
import toml
import os
import shutil

from tools import ApeSphere
from levels import Levels


def apesphere_patches(tool_path, src, dst):
    """
    Install ApeSphere-custom.
    """
    apesphere = ApeSphere(f'{tool_path}/apesphere-custom')
    apesphere.install({
        'ppcinject': f'{tool_path}/ppc-inject',
        'src': src,
        'dst': dst,
        'default_config': True
    })


def apesphere_config(tool_path, dst, rel_patches, party_game, theme_ids,
                     difficulty, music_ids):
    """
    Install a custom config file.
    """
    apesphere = ApeSphere(f'{tool_path}/apesphere-custom')
    apesphere.save_config(dst, {
        'rel_patches': rel_patches,
        'party_game': party_game,
        'theme_ids': theme_ids,
        'difficulty': difficulty,
        'music_ids': music_ids
    })


class SMBProject:
    """
    Wrapper around the project format.
    """

    def __init__(self, config_file):
        self.config = {}
        self.level_list = {}

        with open(config_file) as f:
            self.config = toml.load(f)

        if 'level_list' not in self.config['project']:
            return

        with open(self.config['project']['level_list']) as f:
            self.level_list = toml.load(f)

    def init(self):
        """
        Copy the source directory into the output.
        """
        src = self.config['project']['src']
        dst = self.config['project']['dst']

        shutil.copytree(src, dst)

    def run(self):
        """
        If run is set, invoke the command defined in the project.
        """
        command = self.config['project'].get('run')
        if command:
            os.system(command)

    def build(self):
        """
        Apply the changes described in the project.toml to the `dst` directory.
        """
        # We'll always need Apesphere as this is how a ton of patches are made.
        apesphere_patches(
            self.config['project']['tools'],
            self.config['project']['src'],
            self.config['project']['dst']
        )
        # Next try and load the levels in.
        level_loader = Levels(
            self.level_list,
            self.config['project']['src'],
            self.config['project']['dst']
        )
        level_loader.install_levels()
        level_loader.update_usastr()

        if 'apesphere' in self.config:
            rel_patches = self.config['apesphere'].get('rel', {})
            party_game = self.config['apesphere'].get('partygame', {})
        else:
            rel_patches = {}
            party_game = {}
        music_ids = level_loader.update_music_ids()
        theme_ids = level_loader.update_theme_ids()
        # Now we've decided everything, generate a new apesphere config file.
        apesphere_config(
            self.config['project']['tools'],
            self.config['project']['dst'],
            rel_patches,
            party_game,
            theme_ids,
            {},
            music_ids
        )

    def clean(self):
        """
        Reset back to the initi state.

        Useful incase a change is removed and you want it to go back to its
        initial state.
        """
