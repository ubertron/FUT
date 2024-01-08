from PySide6.QtWidgets import QWidget, QGridLayout, QWidget, QPushButton, QLabel


class GridWidget(QWidget):
    def __init__(self, title: str = '', margin: int = 2, spacing: int = 2):
        super(GridWidget, self).__init__()
        self.setWindowTitle(title)
        self.setLayout(QGridLayout())
        self.layout().setContentsMargins(margin, margin, margin, margin)
        self.layout().setSpacing(spacing)

    def addWidget(self, widget: QWidget, row: int, col: int, row_span: int = 1, col_span: int = 1) -> QWidget:
        """

        :param widget:
        :param row:
        :param col:
        :param row_span:
        :param col_span:
        :return:
        """
        self.layout().addWidget(widget, row, col, row_span, col_span)
        return widget

    def addLabel(self, text: str, row: int, col: int, row_span: int = 1, col_span: int = 1):
        label = QLabel(text)
        return self.addWidget(label, row, col, row_span, col_span)

    def addButton(self, text: str, row: int, col: int, row_span: int = 1, col_span: int = 1):
        button = QPushButton(text)
        return self.addWidget(button, row, col, row_span, col_span)


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    import qdarktheme

    app = QApplication()
    qdarktheme.setup_theme()
    grid_widget = GridWidget('test widget')
    grid_widget.addWidget(QLabel('test1'), 0, 0, 1, 1)
    grid_widget.addButton('test2', 0, 1, 1, 1)
    grid_widget.addWidget(QLabel('test3'), 1, 0, 1, 1)
    grid_widget.addLabel('test4', 1, 1, 1, 1)
    _label = QLabel('test5')
    _label.setStyleSheet('background-color: red')
    grid_widget.addWidget(_label, 2, 0, 1, 2)
    grid_widget.show()
    app.exec()
