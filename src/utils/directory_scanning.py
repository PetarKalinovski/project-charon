import fnmatch
import os
import subprocess
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from constants.directories import SKIP_DIRS


class DirectoryScanner:
    """
    A class to scan directories and find folders based on a given name.
    """

    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.subfolders = self.fast_scandir(root_dir)

    def fast_scandir(self, directory: Path) -> list:
        subfolders = []

        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in SKIP_DIRS]

            for dir_name in dirs:
                subfolders.append(os.path.join(root, dir_name))

        return subfolders

    def find_folder(self, folder_name: str) -> str:
        """
        Searches for a folder with the specified name within the root directory and its subdirectories.

        Args:
            root_dir (Path): The root directory to start the search.
            folder_name (str): The name of the folder to find.

        Returns:
            str: The path to the found folder, or an empty string if not found.
        """

        match_score = {}
        found_folder = None
        for folder in self.subfolders:
            splits = folder.split("/")
            last_folder = splits[-1]
            name_parts = folder_name.split(" ")
            match_score[folder] = 0

            if len(name_parts) == 1:
                if folder_name.lower() in last_folder.lower():
                    print(f"Found folder: {folder}")
                    found_folder = folder
                    break

            if len(name_parts) > 1:
                if all(part.lower() in last_folder.lower() for part in name_parts):
                    print(f"Found folder: {folder}")
                    found_folder = folder
                    break
                for part in name_parts:
                    if part.lower() in last_folder.lower():
                        match_score[folder] += 1

        if found_folder is None:
            best_match = max(match_score, key=match_score.get)
            print(f"Best match: {best_match} with score {match_score[best_match]}")
            found_folder = best_match

        if found_folder is not None:
            return found_folder
        else:
            print(f"Folder '{folder_name}' not found in {self.root_dir}")
            return ""

    def find_files(self, found_folder: Path) -> list:
        """
        Finds all Python files in the specified folder and its subdirectories.
        Args:
            found_folder (Path): The path to the folder to search for Python files.
        Returns:
            list: A list of paths to Python files found in the folder.
        """

        files = []
        for root, _, filenames in os.walk(found_folder):
            if any(fnmatch.fnmatch(root, f"*/{skip_dir}/*") for skip_dir in SKIP_DIRS):
                continue
            k = 0
            for filename in filenames:
                for skip_dir in SKIP_DIRS:
                    if skip_dir in filename:
                        k = 1
                        break
                if k == 0:
                    if filename.endswith(".py") or filename.endswith(".ipynb"):
                        files.append(str(Path(root) / filename))

        return files

    def generate_tree_structure(self, folder_path: Path) -> str:
        """
        Generates a tree structure representation of the directory.

        Args:
            folder_path (Path): The path to the folder to generate the tree structure for.

        Returns:
            str: A string representation of the tree structure.
        """
        result = subprocess.run(
            ["tree", "-l", str(folder_path)],
            capture_output=True,
            text=True,
        )
        return result.stdout
