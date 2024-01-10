from typing import Union
from pandas import DataFrame
from pathlib import Path

from widgets.grid_widget import GridWidget
from widgets.generic_widget import GenericWidget
from fut_utils.fut_manager import FutManager


class FutDataWidget(GridWidget):
    PLAYER_COUNT = 'Player Count'
    TOTAL_VALUE = 'Total Value'
    MEAN = 'Mean'
    MEDIAN = 'Median'
    GOLD = 'Gold'
    SILVER = 'Silver'
    BRONZE = 'Bronze'

    def __init__(self, fut_manager: FutManager):
        super(FutDataWidget, self).__init__()
        self.fut_manager: FutManager = fut_manager
        self.addRow(self.PLAYER_COUNT)
        self.addRow(self.TOTAL_VALUE)
        self.addRow(self.MEAN)
        self.addRow(self.MEDIAN)
        self.addRow(self.GOLD)
        self.addRow(self.SILVER)
        self.addRow(self.BRONZE)

    def addRow(self, label: str):
        num_rows = self.layout().rowCount()
        self.addLabel(label, row=num_rows, col=0)
        self.addLabel('<value>', row=num_rows, col=1)

    def update_data(self, data_path: Path):
        self.fut_manager.data_path = data_path
        self.set_value(self.PLAYER_COUNT, f'{self.fut_manager.player_count:,}')
        self.set_value(self.TOTAL_VALUE, f'{self.fut_manager.total_player_rating:,}')
        self.set_value(self.MEAN, f'{self.fut_manager.mean_player_rating:.1f}')
        self.set_value(self.MEDIAN, self.fut_manager.median_player_rating)
        self.set_value(self.GOLD, self.fut_manager.num_gold)
        self.set_value(self.SILVER, self.fut_manager.num_silver)
        self.set_value(self.BRONZE, self.fut_manager.num_bronze)

    @property
    def row_count(self) -> int:
        return self.layout().rowCount()

    def get_row_index(self, key: str):
        return next(i for i in range(1, self.row_count) if self.layout().itemAtPosition(i, 0).widget().text() == key)

    def set_value(self, key: str, value: Union[str, int]):
        self.layout().itemAtPosition(self.get_row_index(key), 1).widget().setText(str(value))
