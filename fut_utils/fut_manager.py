from pathlib import Path
import pandas as pd
import logging
import matplotlib.pyplot as plt

from pandas.core.frame import DataFrame
from typing import Tuple

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

CLUB_ANALYZER: Path = Path(__file__).parent.joinpath('data/club-analyzer.csv')


class FutManager:
    RATING: str = 'Rating'

    def __init__(self):
        self.data: DataFrame = pd.read_csv(CLUB_ANALYZER.as_posix())
        logging.info(f'Range is {self.rating_range}')
        df = pd.DataFrame({self.RATING: self.data[self.RATING]})
        df[self.RATING].hist(bins=self.bins)
        plt.show()

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


if __name__ == '__main__':
    FutManager()
