from copy import deepcopy

from league_simulator.config import DATASET
from league_simulator.loaders.json_loader import JsonLoader


_BASE_LEAGUE = JsonLoader.load(DATASET)


def get_league():
    return deepcopy(_BASE_LEAGUE)