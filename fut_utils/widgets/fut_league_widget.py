import logging

from PySide6.QtWidgets import QComboBox, QLabel
from PySide6.QtCore import Qt
from collections import OrderedDict

from fut_utils.fut_manager import FutManager
from fut_utils.fut_enums import FutAttr, Rarity
from widgets.generic_widget import GenericWidget
from widgets.grid_widget import GridWidget


logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


class FutLeagueWidget(GenericWidget):
    LEAGUE: str = 'league'

    def __init__(self, fut_manager_ui: GenericWidget):
        super(FutLeagueWidget, self).__init__()
        self.fut_manager_ui = fut_manager_ui
        self.league_combo_box: QComboBox = self.add_widget(QComboBox())
        self.grid_widget: GridWidget = self.add_widget(GridWidget())
        self.add_stretch()
        self.setup_ui()

    def setup_ui(self):
        """
        Set up ui
        """
        self.update_league_combo_box()
        self.league_combo_box_index_changed(self.league_combo_box.currentText())
        self.league_combo_box.currentTextChanged.connect(self.league_combo_box_index_changed)

    def update_league_combo_box(self):
        """
        Update league combo box
        """
        last_league = self.fut_manager_ui.settings.value(self.LEAGUE)
        self.league_combo_box.clear()
        self.league_combo_box.addItems(self.fut_manager_ui.fut_manager.leagues)

        if last_league in self.fut_manager_ui.fut_manager.leagues:
            self.league_combo_box.setCurrentText(last_league)

    def league_combo_box_index_changed(self, arg):
        """
        Event for league combo box selection change
        :param arg:
        """
        self.fut_manager_ui.settings.setValue(self.LEAGUE, arg)
        position_map = self.fut_manager.league_analyser(league=arg)
        info = []
        player_dict = OrderedDict()

        for key, value in position_map.items():
            values = value.iterrows()
            player_data = [self.format_player(row) for i, row in values]
            player_data.sort(key=lambda i: i.lower())
            player_info = []
            idx = 0

            while idx < len(player_data):
                player = player_data[idx]
                count = player_data.count(player)
                player_info.append(f"{player}{f' x{count}' if count > 1 else ''}")
                idx += count

            info.append(f'{key}:\t{", ".join(player_info)}')
            player_dict[key] = player_info

        self.grid_widget.clear()
        row = 0

        for position, info in player_dict.items():
            position_label: QLabel = self.grid_widget.addLabel(position if position else 'Unknown', row=row, col=0)
            position_label.setFixedWidth(80)
            info_label: QLabel = self.grid_widget.addLabel(', '.join(info), row=row, col=1)
            info_label.setWordWrap(True)
            info_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            row += 1

    @staticmethod
    def format_player(row) -> str:
        """
        Returns a string representing a player
        :param row:
        :return:
        """
        rarity = row[FutAttr.rarity.value]
        rarity_tag = f'[{row[FutAttr.rarity.value]}]' if rarity not in (Rarity.common.value, Rarity.rare.value) else ''
        return f'{row[FutAttr.name.value]} {row[FutAttr.surname.value]} [{row[FutAttr.rating.value]}]{rarity_tag}'

    @property
    def fut_manager(self) -> FutManager:
        return self.fut_manager_ui.fut_manager
