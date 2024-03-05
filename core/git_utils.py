import os
from git import Repo
from typing import List
from pathlib import Path

from core import PROJECT_ROOT, DROPBOX


class GitManager:
    def __init__(self):
        self.repo: Repo = Repo(PROJECT_ROOT.as_posix())

    def __repr__(self) -> str:
        info = f'Name: {self.name}'
        info += f'\nRoot: {self.root}'
        return info

    @property
    def name(self) -> str:
        return self.root.name

    @property
    def root(self) -> Path:
        return Path(self.repo.working_tree_dir)

    @property
    def active_branch(self) -> str:
        return self.repo.active_branch

    @property
    def branch_names(self) -> List[str]:
        return [branch.name for branch in self.repo.branches]

    @property
    def commits(self):
        return [commit.hexsha for commit in self.repo.iter_commits()]

    @property
    def files_in_repo(self):
        return [Path(blob[1].path) for blob in self.repo.index.iter_blobs()]

    def check_directory_for_new_files(self, directory: Path) -> List[Path]:
        """
        Finds files in a directory that are not in the repo
        :param directory:
        :return:
        """
        absolute_path = self.root.joinpath(directory)
        local_files = [x.relative_to(absolute_path) for x in absolute_path.iterdir()]
        repo_files = [self.root.joinpath(x) for x in self.files_in_repo]
        filtered = [x.relative_to(absolute_path) for x in repo_files if absolute_path in x.parents]
        new_files = [x for x in local_files if x not in filtered]

        return new_files

    def is_file_in_repo(self, file_path: Path) -> bool:
        """
        Returns True if the passed relative file path is in the repo
        :param file_path:
        :return:
        """
        return file_path in self.files_in_repo

    def add(self, file_path: Path):
        """
        Add a file to the current changelist
        :param file_path:
        """
        if not self.is_file_in_repo(file_path) and self.root.joinpath(file_path).exists():
            self.repo.index.add([file_path])


if __name__ == '__main__':
    git_manager = GitManager()
    print(git_manager)
    my_path = Path('fut_utils/data/club-analyzer_2024_03_04.csv')

    # print(git_manager.commits)
    # print(git_manager.files_in_repo)
    data_directory = Path('fut_utils/data')
    plots_directory = Path('fut_utils/plots')
    # git_manager.check_directory_for_new_files(data_directory)
    git_manager.add(my_path)
