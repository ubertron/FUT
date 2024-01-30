from typing import Union
from pandas import DataFrame
from pathlib import Path
from collections import OrderedDict
import pandas as pd

from widgets.grid_widget import GridWidget
from widgets.generic_widget import GenericWidget
from fut_utils.fut_manager import FutManager


class FutDataWidget(GridWidget):
    PLAYER_COUNT = 'Player Count'
    TOTAL_VALUE = 'Total Value'
    MEAN = 'Mean'
    MEDIAN = 'Median'
    MODE = 'Mode'
    GOLD = 'Gold'
    SILVER = 'Silver'
    BRONZE = 'Bronze'

    def __init__(self, fut_manager: FutManager):
        super(FutDataWidget, self).__init__()
        self.fut_manager: FutManager = fut_manager
        self.add_row(self.PLAYER_COUNT)
        self.add_row(self.TOTAL_VALUE)
        self.add_row(self.MEAN)
        self.add_row(self.MEDIAN)
        self.add_row(self.MODE)
        self.add_row(self.GOLD)
        self.add_row(self.SILVER)
        self.add_row(self.BRONZE)

    def add_row(self, label: str):
        num_rows = self.layout().rowCount()
        self.addLabel(label, row=num_rows, col=0)
        self.addLabel('<value>', row=num_rows, col=1)

    def update_data(self, data_path: Path):
        self.fut_manager.data_path = data_path
        self.set_value(self.PLAYER_COUNT, f'{self.fut_manager.player_count:,}')
        self.set_value(self.TOTAL_VALUE, f'{self.fut_manager.total_player_rating:,}')
        self.set_value(self.MEAN, f'{self.fut_manager.mean_player_rating:.1f}')
        self.set_value(self.MEDIAN, self.fut_manager.median_player_rating)
        self.set_value(self.MODE, self.fut_manager.mode_player_rating)
        self.set_value(self.GOLD, self.fut_manager.num_gold)
        self.set_value(self.SILVER, self.fut_manager.num_silver)
        self.set_value(self.BRONZE, self.fut_manager.num_bronze)

    @property
    def row_count(self) -> int:
        return self.layout().rowCount()

    def get_row_index(self, key: str):
        return next(i for i in range(1, self.row_count) if self.get_item(i, 0) == key)

    def set_value(self, key: str, value: Union[str, int]):
        self.layout().itemAtPosition(self.get_row_index(key), 1).widget().setText(str(value))

    def get_item(self, row: int, column: int) -> str:
        return self.layout().itemAtPosition(row, column).widget().text()

    @property
    def data_to_text(self) -> str:
        data_dict = OrderedDict()

        for i in range(self.row_count):
            if self.layout().itemAtPosition(i, 1) is not None:
                data_dict[self.get_item(i, 0)] = self.get_item(i, 1)

        df = DataFrame(data_dict.items())
        markdown = df.to_markdown(index=False, tablefmt='pipe', colalign=['center']*len(df.columns))

        return '\n'.join(markdown.split('\n')[2:])

    @property
    def data_to_csv(self) -> str:
        data_dict = OrderedDict()

        for i in range(self.row_count):
            if self.layout().itemAtPosition(i, 1) is not None:
                data_dict[self.get_item(i, 0)] = self.get_item(i, 1)

        df = DataFrame(data_dict.items())
        return df.to_csv()
