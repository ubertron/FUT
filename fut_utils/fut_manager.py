import pandas as pd
import os
import logging
import matplotlib.pyplot as plt
import shutil

from datetime import datetime
from enum import Enum
from pandas.core.frame import DataFrame
from pathlib import Path
from typing import Tuple, Optional, Union, List

from core.enums import FileExtension

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

DATA_FILE_STEM = 'club-analyzer'
DATA_DIR: Path = Path(__file__).parent.joinpath('data')
DEFAULT_DATA_FILE: Path = DATA_DIR.joinpath(f'{DATA_FILE_STEM}{FileExtension.csv.value}')
PLOTS_DIR: Path = Path(__file__).parent.joinpath('plots')


class FutAttr(Enum):
    surname: str = 'Lastname'
    name: str = 'Name'
    rating: str = 'Rating'
    position: str = 'Position'
    id: str = 'Id'
    club: str = 'Club'
    league: str = 'League'


class FutManager:
    def __init__(self, data_path: Optional[Path] = DEFAULT_DATA_FILE, use_last_data: bool = True):
        self.use_last_data: bool = use_last_data
        self.data_path: Path or None = data_path

    @property
    def last_data_file(self) -> Path:
        return list(DATA_DIR.glob(f'{DATA_FILE_STEM}*'))[-1]

    @property
    def data_path(self) -> Path or None:
        return self._data_path

    @data_path.setter
    def data_path(self, value: Path or None):
        if value == DEFAULT_DATA_FILE:
            if value.exists():
                self._handle_default_data_file(value)
            else:
                value = None

        if value is None:
            if self.use_last_data:
                self._data_path = self.last_data_file
        else:
            if value.exists():
                self._data_path = value
            else:
                self._data_path = None

    @property
    def data(self) -> DataFrame:
        return pd.read_csv(self.data_path.as_posix())

    def _handle_default_data_file(self, data_path: Path):
        """
        Renames the data file by date
        :param data_path:
        """
        if data_path.exists():
            creation_date = os.path.getmtime(data_path)
            nice_date = datetime.utcfromtimestamp(creation_date).strftime('%Y_%m_%d')
            self.data_path = data_path.parent.joinpath(f'{data_path.stem}_{nice_date}{FileExtension.csv.value}')
            os.rename(data_path.as_posix(), self.data_path.as_posix())

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
        return self.data[FutAttr.rating.value].min(), self.data[FutAttr.rating.value].max()

    @property
    def player_count(self) -> int:
        return len(self.data.index)

    @property
    def total_player_rating(self) -> int:
        return self.player_ratings.sum()

    @property
    def num_gold(self) -> int:
        return len(list(filter(lambda x: 75 <= x <= 100, self.player_ratings.to_list())))

    @property
    def num_silver(self) -> int:
        return len(list(filter(lambda x: 65 <= x <= 74, self.player_ratings.to_list())))

    @property
    def num_bronze(self) -> int:
        return len(list(filter(lambda x: 0 <= x <= 64, self.player_ratings.to_list())))

    @property
    def player_ratings(self) -> List[int]:
        return self.data[FutAttr.rating.value]

    @property
    def histogram_path(self) -> Path:
        return PLOTS_DIR.joinpath(f'{self.data_path.stem}{FileExtension.png.value}')

    def generate_histogram(self):
        """
        Create the histogram image
        """
        if self.data_path is not None:
            self.histogram_path.parent.mkdir(parents=True, exist_ok=True)
            result = pd.DataFrame({FutAttr.rating.value: self.data[FutAttr.rating.value]})
            result[FutAttr.rating.value].hist(bins=self.bins)
            plt.savefig(self.histogram_path)
            plt.show()

    def find_max(self, attribute: FutAttr, value: int, input_data: Optional[DataFrame] = None,
                 format_data: bool = False) -> DataFrame:
        data = input_data if input_data else self.data
        result = data.loc[self.data[attribute.value] <= value]

        if format_data:
            self.format_data(data=result)
        return result

    @staticmethod
    def format_data(data: DataFrame):
        for idx, row in data.iterrows():
            print(f'Index: {idx}\n{row}\n\n')

    def find_value(self, attribute: FutAttr, value: Union[str, int], input_data: Optional[DataFrame] = None,
                   format_data: bool = False) -> DataFrame:
        data = input_data if input_data else self.data
        result = data.loc[data[attribute.value] == value]

        if format_data:
            self.format_data(data=result)

        return result

    def find(self, key_value_pairs: list, first_only: bool = False) -> DataFrame:
        player_list = self.data

        for pair in key_value_pairs:
            key, value = pair
            players = player_list.loc[player_list[key] == value]
            player_list = players

        if first_only:
            self.format_player(player_list)
            return player_list[0]

        return player_list

    def list_clubs(self, input_data: Optional[DataFrame] = None, format_results: bool = False):
        """
        Produces a dictionary with the frequencies of the clubs
        :param input_data:
        :param format_results:
        :return:
        """
        data = input_data if input_data is not None else self.data
        result = self.list_frequencies(key=FutAttr.club, input_data=data)
        if format_results:
            for key, value in result.items():
                print(f'{key}: {value}')
        return result

    def list_leagues(self, input_data: Optional[DataFrame] = None, format_results: bool = False):
        """
        Produces a dictionary with the frequencies of the leagues
        :param input_data:
        :param format_results:
        :return:
        """
        data = input_data if input_data is not None else self.data
        result = self.list_frequencies(key=FutAttr.league, input_data=data)
        if format_results:
            for key, value in result.items():
                print(f'{key}: {value}')
        return result

    def list_frequencies(self, key: FutAttr, input_data: Optional[DataFrame] = None):
        """
        Produces a dictionary with the frequencies of the supplied key in the data
        :param key:
        :param input_data:
        :return:
        """
        data = input_data if input_data is not None else self.data
        result = data[key.value].value_counts().to_dict()
        return result

    @staticmethod
    def format_player(x: DataFrame):
        """
        Print the attributes of a player
        :param x:
        """
        for key, value in x.to_dict().items():
            print(f'{key}: {list(value.values())[0]}')


if __name__ == '__main__':
    fm = FutManager()
    # FutManager().find(key_value_pairs=[(FutManager().RATING, 83)])
    # FutManager().find(key_value_pairs=[(FutManager().POSITION, 'CB')])
    # FutManager(data_path=DATA_PATH).generate_histogram()
    fm.generate_histogram()
    print(fm.total_player_rating)
    # FutManager().find(key_value_pairs=[(FutManager.SURNAME, 'Messi')], first_only=True)
    # FutManager().list_leagues(format_results=True)
    # FutManager().list_clubs()
    # FutManager().find_max(FutAttribute.RATING, 70, format_data=True)
    # print(FutManager().find_value(FutAttribute.SURNAME, 'Messi')['Club'].to_string())
    # fm.list_clubs(input_data=fm.find_max(FutAttr.Rating, value=58), format_results=True)
