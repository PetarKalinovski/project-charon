import sys
from pathlib import Path

from strands import tool

sys.path.append(str(Path(__file__).parent.parent))

from schemas.file_search_returns_schemas import FolderSearchResponse
from utils.config_loader import load_config
from utils.directory_scanning import DirectoryScanner
from utils.callback_hanlder_subagents import log_to_session


@tool
def find_folder_from_name(folder_name: str) -> FolderSearchResponse:
    """
    Find a folder by its name in the project root directory, and all python files in it.
    This function searches for a folder matching the provided name, retrieves all Python files within it,
    and returns a structured response including the project name, folder path, and a tree structure of the directory.

    Args:
        folder_name (str): The name of the project and folder to find.

    Returns:
        dict: A dictionary containing:
            - project_name: The name of the found project directory
            - folder_path: The full path to the found folder
            - files: List of all Python file paths in the project
            - tree_structure: Tree representation of the project structure
            - success: Boolean indicating if the folder was found
    """

    config = load_config()

    log_to_session(
        f"Searching for folder: {folder_name} in {config.files_agent.root_directory}"
    )

    scanner = DirectoryScanner(root_dir=Path(config.files_agent.root_directory))
    found_folder = scanner.find_folder(folder_name)

    if not found_folder:
        log_to_session(
            f'Folder "{folder_name}" not found in {config.files_agent.root_directory}'
        )

        return FolderSearchResponse(
            success=False,
            project_name=None,
            folder_path=None,
            files=[],
            tree_structure=f'Folder "{folder_name}" not found in {config.files_agent.root_directory}',
            message=f'No folder named "{folder_name}" was found.',
        )
    folder_path = Path(found_folder)
    project_name = folder_path.name
    found_files = scanner.find_files(folder_path)

    log_to_session(f"Found folder {found_folder} with folder path: {folder_path}")

    file_paths = [
        str(file_path) for file_path in found_files if str(file_path).endswith(".py")
    ]
    tree_structure = scanner.generate_tree_structure(folder_path)
    return FolderSearchResponse(
        success=True,
        project_name=project_name,
        folder_path=str(folder_path),
        files=file_paths,
        tree_structure=tree_structure,
        message=f'Found project "{project_name}" with {len(file_paths)} Python files.',
    )
