from PySide6.QtWidgets import QLabel, QSizePolicy, QFrame
from PySide6.QtGui import QPixmap, QPainter, QPaintEvent
from PySide6.QtCore import Qt, QPoint, QSize
from pathlib import Path
from typing import Optional


class ImageLabel(QLabel):
    def __init__(self, path: Optional[Path] = None, width: Optional[int] = None, height: Optional[int] = None):
        """
        QLabel containing an image
        :param path: Path
        :param width: int
        :param height: int
        """
        super(ImageLabel, self).__init__()
        self.setFrameStyle(QFrame.StyledPanel)
        self.pixmap = None
        self.path: Path = path
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        if width:
            self.setFixedWidth(width)
        if height:
            self.setFixedHeight(height)

    def paintEvent(self, event: QPaintEvent):
        """
        Override for paintEvent
        :param event:
        """
        if self.path is not None:
            size: QSize = self.size()
            point = QPoint(0, 0)
            scaled_pix = self.pixmap.scaled(size, aspectMode=Qt.AspectRatioMode.KeepAspectRatio,
                                            mode=Qt.TransformationMode.SmoothTransformation)
            point.setX((size.width() - scaled_pix.width()) / 2)
            point.setY((size.height() - scaled_pix.height()) / 2)
            QPainter(self).drawPixmap(point, scaled_pix)

    @property
    def pixmap(self) -> QPixmap:
        return self._pixmap

    @pixmap.setter
    def pixmap(self, arg: QPixmap):
        self._pixmap = arg

    @property
    def path(self) -> Path:
        return self._path

    @path.setter
    def path(self, arg: Path or None):
        self._path = arg

        if arg is not None:
            self.pixmap = QPixmap(arg.as_posix())
            self.setWindowTitle(self.path.stem)

        self.update()


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication, QPushButton
    from widgets.generic_widget import GenericWidget

    app = QApplication()
    image_path1 = Path(r'C:\Users\idavisan\Documents\Projects\FUT\fut_utils\plots\club-analyzer_2024_01_03.png')
    image_path2 = Path(r'C:\Users\idavisan\Documents\Projects\FUT\fut_utils\plots\club-analyzer_2024_01_04.png')
    _widget = GenericWidget()
    _label: ImageLabel = _widget.add_widget(ImageLabel())
    _widget.show()
    _widget.resize(400, 400)
    _label.path = image_path1

    def assign():
        _label.path = image_path2
        print(image_path2)
        _label.update()

    _widget.add_button('click', event=assign)
    # , event=lambda x: print('hey'))
    # _label.path = image_path2
    app.exec()
