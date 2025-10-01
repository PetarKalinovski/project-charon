from typing import Optional

from pydantic import BaseModel, Field


class SleepDataSchema(BaseModel):
    """Schema for sleep data tracking."""

    date: str = Field(..., description="Date of the sleep record in YYYY-MM-DD format")
    total_sleep_time: Optional[int] = Field(
        None, description="Total sleep time in minutes"
    )
    sleep_quality: Optional[str] = Field(
        None,
        description="Self-reported sleep quality (e.g., 'good', 'average', 'poor')",
    )
    notes: Optional[str] = Field(
        None, description="Additional notes about the sleep record"
    )
