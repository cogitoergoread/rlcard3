import pytest
from rlcard3.utils.config_read import Config

def test_conf():
    conf = Config('environ.properties')
    memory_init_size = conf.get_int('memory_init_size')
    assert 1000 == memory_init_size