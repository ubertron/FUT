from PySide6.QtWidgets import QSizePolicy, QComboBox, QLabel, QTabWidget
from typing import List
from pathlib import Path

from fut_utils.widgets.fut_summary_widget import FutSummaryWidget
from fut_utils.widgets.fut_league_widget import FutLeagueWidget
from widgets.generic_widget import GenericWidget
from core.enums import Alignment, FileExtension
from fut_utils.fut_manager import FutManager
from fut_utils import DATA_DIR


class FutManagerUI(GenericWidget):
    TITLE: str = 'FUT Manager'
    SUMMARY: str = 'Summary'
    LEAGUES: str = 'Leagues'

    def __init__(self):
        super(FutManagerUI, self).__init__(title=self.TITLE, margin=4)
        self.fut_manager: FutManager = FutManager(data_path=None, use_last_data=False)
        tab_widget = self.add_widget(QTabWidget())
        tab_widget.addTab(FutSummaryWidget(fut_manager_ui=self), self.SUMMARY)
        tab_widget.addTab(FutLeagueWidget(fut_manager_ui=self), self.LEAGUES)
        self.info_label: QLabel = self.add_label(f'{self.TITLE} ready...')
        self.setup_ui()

    def setup_ui(self):
        """
        Initialize the interface
        """
        self.fut_manager.generate_histogram()   # get latest histogram

    @property
    def data_files(self) -> List[Path]:
        return [x.stem for x in DATA_DIR.glob('club-analyzer*')]


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    import qdarktheme

    app = QApplication()
    qdarktheme.setup_theme()
    fut_manager = FutManagerUI()
    fut_manager.show()
    fut_manager.resize(480, 312)
    app.exec()
