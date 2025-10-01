from typing import Optional
from pydantic import BaseModel, Field


class SubstackPostMetadata(BaseModel):
    """Metadata for a Substack post."""

    title: str = Field(..., description="Title of the post")
    id: str = Field(..., description="Unique identifier for the post")
    post_date: str = Field(..., description="Date when the post was published")
    canonical_url: str = Field(..., description="Canonical URL for the post")
    summary: Optional[str] = Field(
        "", description="Short description or summary of the post"
    )
    content: Optional[str] = Field("", description="Content of the post")
    word_count: Optional[int] = Field(0, description="Word count of the post")
