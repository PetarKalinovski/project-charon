from pydantic import BaseModel, Field


class ModelConfig(BaseModel):
    """Configuration for the LLM model."""

    model_id: str = Field(
        ..., description="Model identifier (e.g., 'openrouter/deepseek/deepseek-r1')"
    )


class FilesAgentConfig(BaseModel):
    """Configuration for the files agent."""

    root_directory: str = Field(
        ..., description="Root directory to search for projects"
    )
    model: ModelConfig = Field(..., description="Model configuration")


class CalendarAgentConfig(BaseModel):
    """Configuration for the calendar agent."""

    model: ModelConfig = Field(
        ...,
        description="Model configuration for calendar agent (e.g., 'openrouter/deepseek/deepseek-r1')",
    )


class BooksAgentConfig(BaseModel):
    """Configuration for the books agent."""

    model: ModelConfig = Field(
        ...,
        description="Model configuration for books agent (e.g., 'openrouter/deepseek/deepseek-r1')",
    )
    book_list_file: str = Field(
        ...,
        description="Path to the book list file (e.g., 'data/book_list.json')",
    )


class MoviesAgentConfig(BaseModel):
    """Configuration for the movies agent."""

    model: ModelConfig = Field(
        ...,
        description="Model configuration for movies agent (e.g., 'openrouter/deepseek/deepseek-r1')",
    )

    movie_list_file: str = Field(
        ..., description="Path to the movie and show list file"
    )


class TaskAgentConfig(BaseModel):
    """Configuration for the task agent"""

    model: ModelConfig = Field(
        ...,
        description="Model configuration for task agent (e.g., 'openrouter/deepseek/deepseek-r1')",
    )


class GitHubAgentConfig(BaseModel):
    """Configuration for the GitHub agent."""

    github_username: str = Field(
        ..., description="GitHub username for the agent to interact with repositories"
    )
    model: ModelConfig = Field(
        ...,
        description="Model configuration for GitHub agent (e.g., 'openrouter/deepseek/deepseek-r1')",
    )


class RecommenderAgentConfig(BaseModel):
    """Configuration for the recommender agent."""

    model: ModelConfig = Field(
        ...,
        description="Model configuration for recommender agent (e.g., 'openrouter/deepseek/deepseek-r1')",
    )
    substack_newsletters_file: str = Field(
        ...,
        description="Directory where Substack newsletters are stored",
    )
    youtube_channels_file: str = Field(
        ...,
        description="Directory where YouTube channels are stored",
    )


class HomeAgentConfig(BaseModel):
    """Configuration for the home agent."""

    model: ModelConfig = Field(
        ...,
        description="Model configuration for home agent (e.g., 'openrouter/deepseek/deepseek-r1')",
    )


class BigBossOrchestratorAgentConfig(BaseModel):
    """Configuration for the Big Boss Orchestrator Agent."""

    model: ModelConfig = Field(
        ...,
        description="Model configuration for Big Boss Orchestrator Agent (e.g., 'openrouter/deepseek/deepseek-r1')",
    )
    sleep_tracking_file: str = Field(
        ...,
        description="Path to the sleep tracking data file (e.g., 'data/sleep_tracking.json')",
    )


class Config(BaseModel):
    """Main configuration schema."""

    files_agent: FilesAgentConfig = Field(..., description="Files agent configuration")
    calendar_agent: CalendarAgentConfig = Field(
        ..., description="Calendar agent configuration"
    )
    books_agent: BooksAgentConfig = Field(..., description="Books agent configuration")
    movies_agent: MoviesAgentConfig = Field(
        ..., description="Movies agent configuration"
    )
    task_agent: TaskAgentConfig = Field(..., description="Task agent configuration")

    github_agent: GitHubAgentConfig = Field(
        ..., description="GitHub agent configuration"
    )
    recommender_agent: RecommenderAgentConfig = Field(
        ..., description="Recommender agent configuration"
    )
    home_agent: HomeAgentConfig = Field(..., description="Home agent configuration")

    big_boss_orchestrator_agent: BigBossOrchestratorAgentConfig = Field(
        ..., description="Big Boss Orchestrator agent configuration"
    )
