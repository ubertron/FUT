import pandas as pd
import os
import logging
import matplotlib.pyplot as plt
import shutil
import statistics

from datetime import datetime
from pandas.core.frame import DataFrame
from pathlib import Path
from typing import Tuple, Optional, Union, List

from core.enums import FileExtension
from core import PROJECT_ROOT
from fut_utils import POSITION_DICT
from fut_utils.fut_enums import FutAttr, League, Rarity

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

DATA_FILE_STEM = 'club-analyzer'
DATA_FILE_FILENAME = f'{DATA_FILE_STEM}{FileExtension.csv.value}'
DATA_DIR: Path = Path(__file__).parent.joinpath('data')
DEFAULT_DATA_FILE: Path = DATA_DIR.joinpath(DATA_FILE_FILENAME)
DOWNLOADED_DATA_FILE: Path = Path.home().joinpath('Downloads', DATA_FILE_FILENAME)
PLOTS_DIR: Path = Path(__file__).parent.joinpath('plots')


class FutManager:
    def __init__(self, data_path: Optional[Path] = DEFAULT_DATA_FILE, use_last_data: bool = True):
        self._handle_downloaded_data_file()
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
        self._data_path = value

        if value == DEFAULT_DATA_FILE:
            if value.exists():
                self._rename_default_data_file(value)
            else:
                value = None

        if value is None:
            self._data_path = self.last_data_file if self.use_last_data else None

    @property
    def data(self) -> DataFrame:
        return pd.read_csv(self.data_path.as_posix())

    def _handle_downloaded_data_file(self):
        if DOWNLOADED_DATA_FILE.exists() and not DEFAULT_DATA_FILE.exists():
            result = self._validate_data_file(DOWNLOADED_DATA_FILE)
            if result:
                shutil.move(DOWNLOADED_DATA_FILE, DEFAULT_DATA_FILE)
            else:
                logging.error('Downloaded data file invalid.')

    @staticmethod
    def _validate_data_file(csv_path: Path):
        data: DataFrame = pd.read_csv(csv_path.as_posix())
        return len(data.index) > 1

    def _rename_default_data_file(self, data_path: Path):
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
        result = self.data[FutAttr.rating.value].min(), self.data[FutAttr.rating.value].max()
        return result

    @property
    def player_count(self) -> int:
        return len(self.data.index)

    @property
    def total_player_rating(self) -> int:
        return self.player_ratings.sum()

    @property
    def mean_player_rating(self) -> float:
        return self.player_ratings.mean()

    @property
    def median_player_rating(self) -> int:
        return int(self.player_ratings.median())

    @property
    def mode_player_rating(self) -> int:
        return statistics.mode(self.player_ratings.tolist())

    @property
    def num_totw(self) -> int:
        return len(self.find_value(attribute=FutAttr.rarity, value=Rarity.totw.value))

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

    def generate_histogram(self, show: bool = False):
        """
        Create the histogram image
        """
        if self.data_path is not None:
            self.histogram_path.parent.mkdir(parents=True, exist_ok=True)
            result = pd.DataFrame({FutAttr.rating.value: self.data[FutAttr.rating.value]})
            result[FutAttr.rating.value].hist(bins=self.bins)
            plt.savefig(self.histogram_path)

            if show:
                plt.show()

    def find_max(self, attribute: FutAttr, value: int, input_data: Optional[DataFrame] = None,
                 format_data: bool = False) -> DataFrame:
        """
        Find the row with the highest value of a given attribute
        :param attribute:
        :param value:
        :param input_data:
        :param format_data:
        :return:
        """
        data = input_data if input_data else self.data
        result = data.loc[self.data[attribute.value] <= value]

        if format_data:
            self.format_data(data=result)
        return result

    @staticmethod
    def format_data(data: DataFrame):
        """
        Log the passed rows of data
        :param data:
        """
        for idx, row in data.iterrows():
            print(f'Index: {idx}\n{row}\n\n')

    def find_value(self, attribute: FutAttr, value: Union[str, int], input_data: Optional[DataFrame] = None,
                   format_data: bool = False) -> DataFrame:
        """
        Find rows with a specific value of a given attribute
        :param attribute:
        :param value:
        :param input_data:
        :param format_data:
        :return:
        """
        data = input_data if input_data else self.data
        result = data.loc[data[attribute.value] == value]

        if format_data:
            self.format_data(data=result)

        return result

    def find(self, key_value_pairs: list, first_only: bool = False) -> DataFrame:
        """
        Find items that match key-value pairs
        :param key_value_pairs:
        :param first_only:
        :return:
        """
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

    def format_league_data(self, input_data: Optional[DataFrame] = None, format_results: bool = False):
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

    def league_analyser(self, league: League or str, format_data: bool = False):
        league = league.value if type(league) is League else league
        df = self.find_value(FutAttr.league, value=league)
        positions = list(set(df[FutAttr.position.value].to_list()))
        position_map = {POSITION_DICT.get(i): self.find([(FutAttr.league.value, league),
                                                         (FutAttr.position.value, i)]) for i in positions}

        if format_data:
            for key, value in position_map.items():
                values = value.iterrows()
                player_data = [f'{row[FutAttr.surname.value]} [{row[FutAttr.rating.value]}]' for i, row in values]
                print(f'{key}: {", ".join(player_data)}')

        return position_map

    @property
    def leagues(self) -> List[str]:
        result = list(set(self.data[FutAttr.league.value].to_list()))
        result.sort()
        return result

    @staticmethod
    def format_player(x: DataFrame):
        """
        Print the attributes of a player
        :param x:
        """
        for key, value in x.to_dict().items():
            print(f'{key}: {list(value.values())[0]}')

    def value_list(self, attr: FutAttr) -> List[str]:
        """
        Returns a unique list of all the values of an attribute
        :param attr:
        :return:
        """
        result = list(set(self.data[attr.value].tolist()))
        result.sort(key=lambda x: str(x).lower())
        return result


if __name__ == '__main__':
    fm: FutManager = FutManager()
    fm.generate_histogram(show=True)
    # print(fm.data.columns)
    # print(fm.value_list(FutAttr.loans))
    # FutManager()._validate_data_file(DOWNLOADED_DATA_FILE)
    # print('\n'.join(fm.leagues))
    # fm.league_analyser(League.d1_arkema, format_data=True)
    # fm.league_analyser(League.wsl)
    # fm.league_analyser(League.serie_a)
    # FutManager().find(key_value_pairs=[(FutManager().RATING, 83)])
    # FutManager().find(key_value_pairs=[(FutManager().POSITION, 'CB')])
    # FutManager(data_path=DATA_PATH).generate_histogram()
    # print(fm.total_player_rating)
    # FutManager().find(key_value_pairs=[(FutManager.SURNAME, 'Messi')], first_only=True)
    # FutManager().list_leagues(format_results=True)
    # FutManager().list_clubs()
    # FutManager().find_max(FutAttribute.RATING, 70, format_data=True)
    # print(FutManager().find_value(FutAttribute.SURNAME, 'Messi')['Club'].to_string())
    # fm.list_clubs(input_data=fm.find_max(FutAttr.Rating, value=58), format_results=True)
    # print(result)
