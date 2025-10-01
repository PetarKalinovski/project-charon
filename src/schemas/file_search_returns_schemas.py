from typing import List, Optional

from pydantic import BaseModel, Field


class FolderSearchResponse(BaseModel):
    """Response schema for find_folder_from_name tool."""

    success: bool = Field(..., description="Whether the folder was found successfully")
    project_name: Optional[str] = Field(
        None, description="Name of the found project directory"
    )
    folder_path: Optional[str] = Field(
        None, description="Full path to the found folder"
    )
    files: List[str] = Field(
        default_factory=list, description="List of all Python file paths in the project"
    )
    tree_structure: str = Field(
        ..., description="Tree representation of the project structure"
    )
    message: str = Field(..., description="Status message describing the result")
