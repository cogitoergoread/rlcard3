''' Doudizhu utils
'''

import os
import json
from collections import OrderedDict

import rlcard3

# Read required docs
ROOT_PATH = rlcard3.__path__[0]

# a map of abstract action to its index and a list of abstract action
with open(os.path.join(ROOT_PATH, 'games/simpledoudizhu/jsondata/action_space.json'), 'r') as file:
    ACTION_SPACE = json.load(file, object_pairs_hook=OrderedDict)
    ACTION_LIST = list(ACTION_SPACE.keys())
