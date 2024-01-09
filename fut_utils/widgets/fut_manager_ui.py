from PySide6.QtWidgets import QSizePolicy, QComboBox, QLabel
from typing import List
from pathlib import Path

from fut_utils.widgets.fut_data_widget import FutDataWidget
from widgets.generic_widget import GenericWidget
from widgets.image_label import ImageLabel
from core.enums import Alignment, FileExtension
from fut_utils import DATA_DIR, PLOTS_DIR
from fut_utils.fut_manager import FutManager


class FutManagerUI(GenericWidget):
    LIST_SIZE: int = 10
    TITLE: str = 'FUT Manager'

    def __init__(self):
        super(FutManagerUI, self).__init__(title=self.TITLE, margin=4)
        self.fut_manager: FutManager = FutManager(data_path=None, use_last_data=False)
        button_bar: GenericWidget = self.add_widget(GenericWidget(alignment=Alignment.horizontal, spacing=2))
        self.data_combo_box: QComboBox = button_bar.add_widget(QComboBox())
        button_bar.add_stretch()
        button_bar.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        data_panel: GenericWidget = self.add_widget(GenericWidget(alignment=Alignment.horizontal))
        self.data_widget: FutDataWidget = data_panel.add_widget(FutDataWidget(fut_manager=self.fut_manager))
        self.histogram: ImageLabel = data_panel.add_widget(ImageLabel(None))
        self.info_label: QLabel = self.add_label(f'{self.TITLE} ready...')
        self.setup_ui()

    def setup_ui(self):
        """
        Initialize the widgets
        """
        self.update_data_combo_box()
        self.update_data()
        self.data_combo_box.currentTextChanged.connect(self.data_combo_box_changed)

    @property
    def current_data_path(self) -> Path:
        return DATA_DIR.joinpath(f'{self.data_combo_box.currentText()}{FileExtension.csv.value}')

    @property
    def current_histogram(self) -> Path:
        return PLOTS_DIR.joinpath(f'{self.data_combo_box.currentText()}{FileExtension.png.value}')

    def data_combo_box_changed(self):
        """
        Event for data combo box
        """
        self.update_data()

    def update_data(self):
        """
        Update the data widget and histogram
        """
        self.data_widget.update_data(data_path=self.current_data_path)

        if not self.current_histogram.exists():
            self.fut_manager.generate_histogram()

        self.histogram.path = self.current_histogram

    def update_data_combo_box(self):
        """
        Get a list of the data files and populate the combo box
        """
        data_files = self.data_files[-min(len(self.data_files), self.LIST_SIZE):]
        data_files.reverse()
        self.data_combo_box.clear()
        self.data_combo_box.addItems(data_files)

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
