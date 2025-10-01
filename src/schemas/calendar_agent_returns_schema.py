from typing import List, Optional

from pydantic import BaseModel, Field


class CalendarEventResponse(BaseModel):
    """Schema for a calendar event response from get_events."""

    start: str = Field(..., description="Start time of the event (ISO format)")
    end: str = Field(..., description="End time of the event (ISO format)")
    summary: str = Field(..., description="Summary/title of the event")


class CalendarEventsListResponse(BaseModel):
    """Schema for a list of calendar events."""

    events: List[CalendarEventResponse] = Field(
        ..., description="List of calendar events"
    )
    total_count: int = Field(..., description="Total number of events")


class CalendarCreationReturn(BaseModel):
    """Schema for calendar event creation response."""

    status: str = Field(..., description="Status of the event creation")
    message: str = Field(
        ..., description="Message describing the result of the event creation"
    )
    event_link: str = Field(..., description="Link to the created event")
    event_id: str = Field(..., description="ID of the created event")


class CalendarEventInput(BaseModel):
    """Schema for calendar event input (for creation)."""

    title: str = Field(..., description="Title of the event")
    start_time: str = Field(
        ..., description="Start time of the event in 'YYYY-MM-DDTHH:MM:SS' format"
    )
    end_time: str = Field(
        ..., description="End time of the event in 'YYYY-MM-DDTHH:MM:SS' format"
    )
    description: Optional[str] = Field("", description="Description of the event")
    location: Optional[str] = Field("", description="Location of the event")
