from pathlib import Path
import pandas as pd
import logging
import matplotlib.pyplot as plt

from pandas.core.frame import DataFrame
from typing import Tuple

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

# CLUB_ANALYZER: Path = Path(__file__).parent.joinpath('data/club-analyzer_2024_01_03.csv')
CLUB_ANALYZER: Path = Path(__file__).parent.joinpath('data/club-analyzer_2024_01_03.csv')
PLOTS_DIR: Path = Path(__file__).parent.joinpath('plots')


class FutManager:
    SURNAME: str = 'Lastname'
    NAME: str = 'Name'
    RATING: str = 'Rating'
    POSITION: str = 'Position'
    ID: str = 'Id'

    def __init__(self, data_path: Path):
        self.data_path: Path = data_path
        self.data: DataFrame = pd.read_csv(data_path.as_posix())

    @property
    def bins(self) -> list[int]:
        rating_range = list(range(*self.rating_range))
        rating_range.append(rating_range[-1] + 1)
        return rating_range

    @property
    def columns(self):
        return self.data.columns

    @property
    def rating_range(self) -> Tuple[int]:
        return self.data[self.RATING].min(), self.data[self.RATING].max()

    @property
    def histogram_path(self) -> Path:
        return PLOTS_DIR.joinpath(f'{self.data_path.stem}.png')

    def generate_histogram(self):
        """
        Create the histogram image
        """
        self.histogram_path.parent.mkdir(parents=True, exist_ok=True)
        df = pd.DataFrame({self.RATING: self.data[self.RATING]})
        df[self.RATING].hist(bins=self.bins)
        plt.savefig(self.histogram_path)
        plt.show()

    def find(self, key_value_pairs: list):
        player_list = self.data

        for pair in key_value_pairs:
            key, value = pair
            players = player_list.loc[player_list[key] == value]
            player_list = players

        print(self.data.head(1)[self.NAME], self.data.head(1)[self.SURNAME], self.data.head(1)[self.POSITION])
        # print(self.data.head(1)[self.POSITION])
        print(self.columns)
        # print(player_list)
        return player_list


if __name__ == '__main__':
    # FutManager().find(key_value_pairs=[(FutManager().RATING, 83)])
    # FutManager().find(key_value_pairs=[(FutManager().POSITION, 'CB')])
    FutManager(data_path=CLUB_ANALYZER).generate_histogram()
