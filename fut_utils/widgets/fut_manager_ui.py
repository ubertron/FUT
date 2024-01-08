from PySide6.QtWidgets import QSizePolicy, QComboBox, QLabel
from typing import List
from pathlib import Path

from fut_utils.widgets.fut_data_widget import FutDataWidget
from widgets.generic_widget import GenericWidget
from core.enums import Alignment, FileExtension
from fut_utils import DATA_DIR


class FutManagerUI(GenericWidget):
    def __init__(self):
        super(FutManagerUI, self).__init__(title='FUT Manager', margin=4)
        button_bar: GenericWidget = self.add_widget(GenericWidget(alignment=Alignment.horizontal, spacing=2))
        self.refresh_button = button_bar.add_button('Refresh')
        self.data_combo_box: QComboBox = button_bar.add_widget(QComboBox())
        button_bar.add_stretch()
        button_bar.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.data_widget: FutDataWidget = self.add_widget(FutDataWidget())
        self.add_stretch()
        self.info_label: QLabel = self.add_label('Fut Manager ready...')
        self.setup_ui()

    def setup_ui(self):
        self.update_data_combo_box()
        self.update_data()
        self.data_combo_box.currentTextChanged.connect(self.data_combo_box_changed)

    @property
    def current_data_path(self) -> Path:
        return DATA_DIR.joinpath(f'{self.data_combo_box.currentText()}{FileExtension.csv.value}')

    def data_combo_box_changed(self):
        self.update_data()

    def update_data(self):
        self.data_widget.update_data(data_path=self.current_data_path)

    def update_data_combo_box(self):
        # get up to last 5 data files
        data_files = self.data_files[-min(len(self.data_files), 5):]
        data_files.reverse()
        # populate combo box
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
    fut_manager.resize(320, 160)
    # print(fut_manager.data_files)
    app.exec()
