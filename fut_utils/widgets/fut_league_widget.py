from PySide6.QtWidgets import QComboBox

from fut_utils.fut_manager import FutManager
from fut_utils.fut_enums import FutAttr
from widgets.generic_widget import GenericWidget


class FutLeagueWidget(GenericWidget):
    def __init__(self, fut_manager_ui: GenericWidget):
        super(FutLeagueWidget, self).__init__()
        self.fut_manager_ui = fut_manager_ui
        self.league_combo_box: QComboBox = self.add_widget(QComboBox())
        self.info_label = self.add_label('<info>')
        self.setup_ui()

    def setup_ui(self):
        self.update_league_combo_box()
        self.league_combo_box.currentTextChanged.connect(self.update_info)
        self.info_label.setWordWrap(True)
        self.update_info(self.league_combo_box.currentText())

    def update_league_combo_box(self):
        self.league_combo_box.clear()
        self.league_combo_box.addItems(self.fut_manager_ui.fut_manager.leagues)

    def update_info(self, arg):
        position_map = self.fut_manager.league_analyser(league=arg)
        info = []

        for key, value in position_map.items():
            values = value.iterrows()
            player_data = [f'{row[FutAttr.surname.value]} [{row[FutAttr.rating.value]}]' for i, row in values]
            info.append(f'{key}: {", ".join(player_data)}')

        self.info_label.setText('\n'.join(info))

    @property
    def fut_manager(self) -> FutManager:
        return self.fut_manager_ui.fut_manager
