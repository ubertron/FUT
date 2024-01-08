import platform

from PySide6.QtWidgets import QWidget, QApplication, QLabel, QLayout, QPushButton, QHBoxLayout, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
from typing import Optional, Callable
from core.enums import Alignment


class GenericWidget(QWidget):
    ICON_SIZE: int = 16

    def __init__(self, title: str = None, alignment: Alignment = Alignment.vertical, margin: int = 0, spacing: int = 0,
                 parent: Optional[QWidget] = None):
        """
        Generic widget
        :param title: Optional[str]
        :param alignment: Alignment
        :param margin: int
        :param spacing: int
        :param parent: int
        """

        super(GenericWidget, self).__init__(parent=parent)

        self.setWindowTitle(title)
        self.setLayout(QVBoxLayout() if alignment == alignment.vertical else QHBoxLayout())
        self.set_margin(margin)
        self.set_spacing(spacing)
        self.setStyleSheet("QToolTip {background-color: black; color: white;  border: black solid 1px}")

    def add_widget(self, widget: QWidget) -> QWidget:
        """
        Add a widget to the widget
        @param widget:
        @return:
        """
        self.layout().addWidget(widget)
        return widget

    def add_label(self, text: str = "") -> QLabel:
        """
        Add a label to the widget
        @param text:
        @return:
        """
        return self.add_widget(QLabel(text))

    def add_button(self, text: str, tool_tip: str = None, event: Optional[Callable] = None) -> QPushButton:
        """
        Add a QPushButton to the layout
        @param text: str
        @param tool_tip: str
        @param event: slot method
        @return: QPushbutton
        """
        button = QPushButton(text)
        button.setToolTip(tool_tip)
        if event:
            button.clicked.connect(event)
        return self.add_widget(button)

    def replace_layout(self, layout: QLayout):
        """
        Replace the widget layout with a new layout item
        :param layout:
        """
        QWidget().setLayout(self.layout())
        self.setLayout(layout)

    def clear_layout(self, layout: Optional[QLayout] = None):
        """
        Recursive function to clear generic_widgets from the layout
        :param layout: specify a particular layout or top layout is assumed
        """
        if not layout:
            layout = self.layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.clear_layout(item.layout())

    def add_stretch(self):
        """
        Add a stretch item to the layout
        """
        self.layout().addStretch(True)

    def add_spacing(self, value: int):
        """
        Add spacing to the layout
        :param value: size of the spacing
        """
        self.layout().addSpacing(value)

    def set_margin(self, value: int):
        """
        Set widget margin
        :param value:
        """
        self.layout().setContentsMargins(value, value, value, value)

    def set_spacing(self, value: int):
        """
        Set widget spacing
        :param value:
        """
        self.layout().setSpacing(value)


if __name__ == "__main__":
    import sys
    import qdarktheme
    from datetime import datetime

    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    _widget = GenericWidget('Test Widget', alignment=Alignment.horizontal, spacing=4, margin=2)
    _button = _widget.add_button('Click Me', 'Get the time')
    _label = _widget.add_label()
    _button.clicked.connect(lambda _: _label.setText(datetime.now().strftime('%m/%d/%Y %H:%M:%S')))
    _widget.setMinimumWidth(240)
    _widget.show()
    sys.exit(app.exec())
