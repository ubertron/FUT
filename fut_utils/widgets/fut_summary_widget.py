from PySide6.QtWidgets import QSizePolicy, QComboBox, QLabel
from typing import List
from pathlib import Path

from core.enums import Alignment, FileExtension
from fut_utils.fut_manager import FutManager
from fut_utils.widgets.fut_data_widget import FutDataWidget
from fut_utils import DATA_DIR, PLOTS_DIR
from widgets.generic_widget import GenericWidget
from widgets.image_label import ImageLabel


class FutSummaryWidget(GenericWidget):
    LIST_SIZE: int = 10

    def __init__(self, fut_manager_ui: GenericWidget):
        super(FutSummaryWidget, self).__init__()
        self.fut_manager_ui = fut_manager_ui
        button_bar: GenericWidget = self.add_widget(GenericWidget(alignment=Alignment.horizontal, spacing=2))
        self.data_combo_box: QComboBox = button_bar.add_widget(QComboBox())
        button_bar.add_stretch()
        button_bar.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        data_panel: GenericWidget = self.add_widget(GenericWidget(alignment=Alignment.horizontal))
        self.data_widget: FutDataWidget = data_panel.add_widget(FutDataWidget(fut_manager=self.fut_manager))
        self.histogram: ImageLabel = data_panel.add_widget(ImageLabel(None))
        self.setup_ui()

    def setup_ui(self):
        self.update_data_combo_box()
        self.update_data()
        self.data_combo_box.currentTextChanged.connect(self.data_combo_box_changed)
        self.data_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

    @property
    def fut_manager(self) -> FutManager:
        return self.fut_manager_ui.fut_manager

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
        data_files = self.fut_manager_ui.data_files[-min(len(self.fut_manager_ui.data_files), self.LIST_SIZE):]
        data_files.reverse()
        self.data_combo_box.clear()
        self.data_combo_box.addItems(data_files)