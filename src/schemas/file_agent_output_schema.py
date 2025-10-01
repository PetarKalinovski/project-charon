from typing import List, Optional

from pydantic import BaseModel, Field


class FileAgentOutputSchema(BaseModel):
    """Schema for the output of file agent operations."""

    success: bool = Field(..., description="Indicates if the operation was successful")
    message: str = Field(..., description="Status message describing the result")
    project_name: Optional[str] = Field(
        None, description="Name of the project entered by the user"
    )
    folder_path: Optional[str] = Field(
        None, description="Full path to the project folder"
    )
    files: List[str] = Field(
        default_factory=list, description="List of file paths processed by the agent"
    )
    estimated_time: Optional[str] = Field(
        None,
        description="Estimated time for the task completion",
        examples=["Approximately 5 minutes", " 2 hours", "16 minutes"],
    )
