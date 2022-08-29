import logging
from configparser import ConfigParser
from os import path

SRC_DIR = path.split(__file__)[0]
CONFIG_DIR = path.realpath(path.join(SRC_DIR, '../config/'))
CONFIG_FILE = path.join(CONFIG_DIR, "config.ini")

__all__ = ['config']


def config(section='services', filename=None):
    filename = filename if filename is not None else CONFIG_FILE

    parser = ConfigParser()
    parser.read(filename)

    cfg = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            cfg[param[0]] = param[1]
        logging.debug(cfg)
    else:
        raise FileNotFoundError('Section {0} not found in the {1} file'.format(section, filename))

    return cfg
