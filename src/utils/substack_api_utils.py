from substack_api import Newsletter, Post
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.schemas.substack_schema import SubstackPostMetadata


def get_recent_posts(newsletter_url: str, limit: int = 5) -> list:
    """
    Fetch recent posts from a Substack newsletter.

    Args:
        newsletter_url (str): The URL of the Substack newsletter.
        limit (int): The number of recent posts to fetch.

    Returns:
        List of recent posts.
    """

    newsletter = Newsletter("https://www.noahpinion.blog/")
    return newsletter.get_posts(limit=limit)


def get_post_metadata(post: Post) -> SubstackPostMetadata:
    """
    Extract metadata from a Substack post.

    Args:
        post (Post): The Substack post object.

    Returns:
        Dictionary containing post metadata.
    """
    metadata = post.get_metadata()

    return SubstackPostMetadata(
        title=metadata["title"],
        id=str(metadata["id"]),
        post_date=metadata["post_date"],
        canonical_url=metadata["canonical_url"],
        summary=metadata["description"] or "",
        content=metadata["truncated_body_text"],
        word_count=metadata.get("wordcount", 0),
    )


def get_post_metadata_from_newsletter(newsletter_url: str, limit: int = 5) -> list:
    """
    Get a list of posts from a Substack newsletter.

    Args:
        newsletter_url (str): The URL of the Substack newsletter.
        limit (int): The number of posts to retrieve.

    Returns:
        List of dictionaries containing post metadata.
    """
    newsletter = Newsletter(newsletter_url)
    posts = newsletter.get_posts(limit=limit)

    return [get_post_metadata(post) for post in posts]
