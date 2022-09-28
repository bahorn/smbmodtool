"""
Level Manager
"""
import copy
import shutil
from defaults import default_music_id, default_theme_id


class Levels:
    def __init__(self, config, src, dst):
        self.config = config
        self.src = src
        self.dst = dst

    def update_usastr(self):
        """
        USA str for the english language version of the game
        """
        data = []
        # load the existing level list
        with open(f'{self.src}/files/stgname/usa.str') as f:
            data = f.read().split('\n')
        # Patch for each level
        for _, level in self.config['levels'].items():
            data[level['slot']] = level['name'].upper()
        # Save the new level names
        with open(f'{self.dst}/files/stgname/usa.str', 'w') as f:
            f.write("\n".join(data))

    def install_levels(self):
        """
        Copy levels into the game.
        """
        stage_dir = f'{self.dst}/files/stage'
        for _, level in self.config['levels'].items():
            slot = level['slot']
            gma = level['gma']
            tpl = level['tpl']
            lz = level['lz']
            shutil.copy(gma, f'{stage_dir}/st{slot:03}.gma')
            shutil.copy(tpl, f'{stage_dir}/st{slot:03}.tpl')
            shutil.copy(lz, f'{stage_dir}/STAGE{slot:03}.lz')

    def update_music_ids(self):
        """
        Music IDs for ApeSphere
        """
        music_ids = copy.deepcopy(default_music_id)
        for _, level in self.config['levels'].items():
            if 'music_id' in level:
                music_ids[level['slot']] = level['music_id']
        return music_ids

    def update_theme_ids(self):
        """
        Theme ID for ApeSphere
        """
        theme_ids = copy.deepcopy(default_theme_id)
        for _, level in self.config['levels'].items():
            if 'theme_id' in level:
                theme_ids[level['slot']] = level['theme_id']
        return theme_ids
