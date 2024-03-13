import logging
from PySide6.QtWidgets import QSizePolicy, QComboBox, QLabel, QTabWidget
from PySide6.QtCore import QSettings
from PySide6.QtGui import QPixmap
from typing import List
from pathlib import Path

from fut_utils.fut_widgets.fut_summary_widget import FutSummaryWidget
from fut_utils.fut_widgets.fut_league_widget import FutLeagueWidget
from widgets.generic_widget import GenericWidget
from core.enums import Alignment, FileExtension
from fut_utils.fut_manager import FutManager
from fut_utils import DATA_DIR
from core import image_path, CREATOR

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


class FutManagerUI(GenericWidget):
    TITLE: str = 'FUT Manager'
    SUMMARY: str = 'Summary'
    LEAGUES: str = 'Leagues'
    TAB_INDEX: str = 'tab_index'

    def __init__(self):
        super(FutManagerUI, self).__init__(title=self.TITLE, margin=4)
        self.settings: QSettings = QSettings(CREATOR, self.TITLE)
        logging.debug(self.settings.fileName())
        self.fut_manager: FutManager = FutManager()
        self.tab_widget: QTabWidget = self.add_widget(QTabWidget())
        self.tab_widget.addTab(FutSummaryWidget(fut_manager_ui=self), self.SUMMARY)
        self.tab_widget.addTab(FutLeagueWidget(fut_manager_ui=self), self.LEAGUES)
        self.info_label: QLabel = self.add_label(f'{self.TITLE} ready...')
        self.setup_ui()

    def setup_ui(self):
        """
        Initialize the interface
        """
        self.fut_manager.generate_histogram()   # get latest histogram
        self.tab_widget.setCurrentIndex(self.settings.value(self.TAB_INDEX, 0))
        self.tab_widget.currentChanged.connect(self.tab_widget_changed)
        self.setStyleSheet('font: 10pt "Verdana";')

    @property
    def data_files(self) -> List[Path]:
        result = [x.stem for x in DATA_DIR.glob('club-analyzer*')]
        result.sort()
        return result

    def tab_widget_changed(self, arg):
        self.settings.setValue(self.TAB_INDEX, arg)


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    import qdarktheme

    app = QApplication()
    qdarktheme.setup_theme()
    app.setWindowIcon(QPixmap(image_path('fut_logo.png').as_posix()))
    fut_manager = FutManagerUI()
    fut_manager.show()
    fut_manager.resize(800, 560)
    app.exec()
