from pathlib import Path

CREATOR: str = 'Robosoft'
DATA_DIR: Path = Path(__file__).parent.joinpath('data')
PLOTS_DIR: Path = Path(__file__).parent.joinpath('plots')
POSITION_DICT: dict = {
    0: 'GK',
    2: 'RWB',
    3: 'RB',
    5: 'CB',
    7: 'LB',
    8: 'LWB',
    10: 'CDM',
    12: 'RM',
    14: 'CM',
    16: 'LM',
    18: 'CAM',
    21: 'CF',
    23: 'RW',
    25: 'ST',
    27: 'LW',
}
