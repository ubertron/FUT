from pathlib import Path

PROJECT_ROOT: Path = Path(__file__).parents[1]
DROPBOX: Path = Path.home().joinpath('Dropbox')
IMAGE_DIR: Path = PROJECT_ROOT.joinpath('images')


def image_path(image_name: str) -> Path:
    return IMAGE_DIR.joinpath(image_name)


CREATOR: str = 'Robosoft'
