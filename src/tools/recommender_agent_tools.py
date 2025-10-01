from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from src.utils.substack_api_utils import (
    get_recent_posts,
    get_post_metadata,
)
from src.utils.youtube_api_utils import YouTubeMonitor
from strands import tool
import json
from src.utils.config_loader import load_config
from src.utils.callback_hanlder_subagents import log_to_session


@tool
def add_substack_newsletter_to_monitor(
    newsletter_url: str, note_about_newsletter: str
) -> str:
    """
    Add a Substack newsletter to the monitoring list.

    Args:
        newsletter_url (str): The URL of the Substack newsletter.
        note_about_newsletter (str): A note about the newsletter. For example, for the semi-analysis substack, you would write "Dylan Patel's substack".

    Returns:
        str: Confirmation message.
    """
    config = load_config()
    if not config.recommender_agent.substack_newsletters_file:
        log_to_session(
            "Substack newsletters file is not configured in the project config."
        )
        return "Substack newsletters file is not configured in the project config."
    path_url = config.recommender_agent.substack_newsletters_file
    try:
        with open(path_url) as file:
            newsletters = json.load(file)
    except FileNotFoundError:
        log_to_session(f"File {path_url} not found")
        newsletters = []

    if newsletter_url in newsletters:
        log_to_session(
            f"Newsletter {newsletter_url} is already in the monitoring list."
        )
        return f"Newsletter {newsletter_url} is already in the monitoring list."

    newsletters.append({newsletter_url: note_about_newsletter})

    with open(path_url, "w") as file:
        json.dump(newsletters, file)
    log_to_session(
        f"Newsletter {newsletter_url} has been added to the monitoring list."
    )

    return f"Newsletter {newsletter_url} has been added to your monitoring list."


@tool
def get_all_newsletters() -> list:
    """
    Retrieve all Substack newsletters from the monitoring list.

    Returns:
        list: List of Substack newsletter URLs.
    """
    config = load_config()
    if not config.recommender_agent.substack_newsletters_file:
        log_to_session(
            "Substack newsletters directory is not configured in the project config."
        )
        return [
            "Substack newsletters directory is not configured in the project config."
        ]
    path_url = config.recommender_agent.substack_newsletters_file

    try:
        with open(path_url) as file:
            newsletters = json.load(file)
        log_to_session(
            f"Retrieved {len(newsletters)} newsletters from the monitoring list."
        )
        return newsletters
    except FileNotFoundError:
        log_to_session(f"File {path_url} not found")
        return []


@tool
def get_recent_posts_from_newsletter(newsletter_url: str, limit: int = 5) -> list:
    """
    Get recent posts from a Substack newsletter.

    Args:
        newsletter_url (str): The URL of the Substack newsletter.
        limit (int): The number of recent posts to fetch.

    Returns:
        list: List of recent posts with metadata.
    """
    try:
        posts = get_recent_posts(newsletter_url, limit)
        log_to_session(f"Retrieved {len(posts)} recent posts from {newsletter_url}.")
        metadata = [get_post_metadata(post) for post in posts]
        log_to_session(f"Extracted metadata for {len(metadata)} posts.")
        return metadata

    except Exception as e:
        log_to_session(f"Error fetching posts from {newsletter_url}: {e}")
        return [f"Error fetching posts from {newsletter_url}: {e}"]


@tool
def get_recent_youtube_videos(channel_url: str, limit: int = 10) -> list:
    """
    Get recent videos from a YouTube channel.
    Args:
        channel_url (str): The URL or handle of the YouTube channel.
        limit (int): The number of recent videos to fetch.
    Returns:
        list: List of recent videos with metadata.
    """
    try:
        youtube_monitor = YouTubeMonitor()
        channel_id = youtube_monitor.get_channel_id_from_url(channel_url)
        videos = youtube_monitor.get_recent_videos(channel_id, limit)
        log_to_session(
            f"Retrieved {len(videos)} recent videos from channel {channel_id}."
        )
        return videos
    except Exception as e:
        log_to_session(f"Error fetching videos from channel {channel_id}: {e}")
        return [f"Error fetching videos from channel {channel_id}: {e}"]


@tool
def get_all_monitored_youtube_channels() -> list:
    """
    Retrieve all monitored YouTube channels.

    Returns:
        list: List of YouTube channel URLs.
    """
    config = load_config()
    if not config.recommender_agent.youtube_channels_file:
        log_to_session("YouTube channels file is not configured in the project config.")
        return ["YouTube channels file is not configured in the project config."]
    path_url = config.recommender_agent.youtube_channels_file

    try:
        with open(path_url) as file:
            channels = json.load(file)
        log_to_session(f"Retrieved {len(channels)} monitored YouTube channels.")
        return channels
    except FileNotFoundError:
        log_to_session(f"File {path_url} not found")
        return []


@tool
def add_youtube_channel_to_monitor(channel_url: str, note_about_channel: str) -> str:
    """
    Add a YouTube channel to the monitoring list.

    Args:
        channel_url (str): The URL or handle of the YouTube channel.
        note_about_channel (str): A note about the YouTube channel. For example, for the Ezra Klein show, you would write "Ezra Klein's show (Favorite Podcast)".

    Returns:
        str: Confirmation message.
    """
    config = load_config()
    if not config.recommender_agent.youtube_channels_file:
        log_to_session(
            "YouTube channels directory is not configured in the project config."
        )
        return "YouTube channels directory is not configured in the project config."

    path_url = config.recommender_agent.youtube_channels_file

    try:
        with open(path_url) as file:
            channels = json.load(file)
    except FileNotFoundError:
        log_to_session(f"File {path_url} not found")
        channels = []

    if channel_url in channels:
        log_to_session(f"Channel {channel_url} is already in the monitoring list.")
        return f"Channel {channel_url} is already in the monitoring list."

    channels.append({channel_url: note_about_channel})

    with open(path_url, "w") as file:
        json.dump(channels, file)
    log_to_session(f"Channel {channel_url} has been added to the monitoring list.")

    return f"Channel {channel_url} has been added to your monitoring list."
