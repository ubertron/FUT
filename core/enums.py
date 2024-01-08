from enum import Enum, unique, auto


class FileExtension(Enum):
    csv = '.csv'
    png = '.png'


@unique
class Alignment(Enum):
    horizontal = auto()
    vertical = auto()
