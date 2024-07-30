import json
import re

from pprint import pprint

from processors import *
from transformers import *


with open("../src/AnAdventure/data/aa/function/spawn/end/phantom.mcab") as file:
    pprint(Transformers.apply_all(make_blocks(Processors.apply_all(file.read()))))
