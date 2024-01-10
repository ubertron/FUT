import logging

from PySide6.QtWidgets import QComboBox

from fut_utils.fut_manager import FutManager
from fut_utils.fut_enums import FutAttr
from widgets.generic_widget import GenericWidget


logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


class FutLeagueWidget(GenericWidget):
    LEAGUE: str = 'league'

    def __init__(self, fut_manager_ui: GenericWidget):
        super(FutLeagueWidget, self).__init__()
        self.fut_manager_ui = fut_manager_ui
        self.league_combo_box: QComboBox = self.add_widget(QComboBox())
        self.info_label = self.add_label('<info>')
        self.setup_ui()

    def setup_ui(self):
        self.update_league_combo_box()
        self.info_label.setWordWrap(True)
        self.league_combo_box_index_changed(self.league_combo_box.currentText())
        self.league_combo_box.currentTextChanged.connect(self.league_combo_box_index_changed)

    def update_league_combo_box(self):
        last_league = self.fut_manager_ui.settings.value(self.LEAGUE)
        self.league_combo_box.clear()
        self.league_combo_box.addItems(self.fut_manager_ui.fut_manager.leagues)

        if last_league in self.fut_manager_ui.fut_manager.leagues:
            self.league_combo_box.setCurrentText(last_league)

    def league_combo_box_index_changed(self, arg):
        self.fut_manager_ui.settings.setValue(self.LEAGUE, arg)
        position_map = self.fut_manager.league_analyser(league=arg)
        info = []

        for key, value in position_map.items():
            values = value.iterrows()
            player_data = [f'{row[FutAttr.surname.value]} [{row[FutAttr.rating.value]}]' for i, row in values]
            info.append(f'{key}:\t{", ".join(player_data)}')

        self.info_label.setText('\n'.join(info))

    @property
    def fut_manager(self) -> FutManager:
        return self.fut_manager_ui.fut_manager
