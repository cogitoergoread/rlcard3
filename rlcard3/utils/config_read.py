"""
Load configuration files values
See: https://stackoverflow.com/questions/27945073/how-to-read-properties-file-in-python/34988437
"""
import configparser
import os
import rlcard3

ROOT_PATH = os.path.join(rlcard3.__path__[0], '..', 'examples')
class Config:

    def __init__(self, config_file):
        self.config = self._read_config([os.path.join(ROOT_PATH, config_file)])

    # a simple function to read an array of configuration files into a config object
    @staticmethod
    def _read_config(cfg_files):
        if cfg_files is not None:
            config = configparser.RawConfigParser()

            # merges all files into a single config
            for i, cfg_file in enumerate(cfg_files):
                print(cfg_file)
                if os.path.exists(cfg_file):
                    config.read(cfg_file)

            return config

    def get_int(self, key: str):
        """
        Return the value of the config key
        :param key: The key
        :return: The value
        """
        return int(self.config.get('global', key))
