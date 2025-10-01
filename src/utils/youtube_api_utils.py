from googleapiclient.discovery import build
import os


class YouTubeMonitor:
    def __init__(self):
        """Initialize the YouTube API client with the API key."""
        api_key = os.getenv("YOUTUBE_API_KEY")
        self.youtube = build("youtube", "v3", developerKey=api_key)

    def get_recent_videos(self, channel_id: str, limit: int = 10):
        """Fetch recent videos from a YouTube channel"""
        channel_response = (
            self.youtube.channels().list(part="contentDetails", id=channel_id).execute()
        )

        uploads_playlist = channel_response["items"][0]["contentDetails"][
            "relatedPlaylists"
        ]["uploads"]

        playlist_response = (
            self.youtube.playlistItems()
            .list(part="snippet", playlistId=uploads_playlist, maxResults=limit)
            .execute()
        )

        video_ids = [
            item["snippet"]["resourceId"]["videoId"]
            for item in playlist_response["items"]
        ]

        videos_response = (
            self.youtube.videos()
            .list(part="snippet,contentDetails,statistics", id=",".join(video_ids))
            .execute()
        )

        return videos_response["items"]

    def get_channel_id_from_url(self, channel_url_or_handle):
        """Convert any YouTube channel URL/handle to channel ID"""

        if "@" in channel_url_or_handle:
            handle = channel_url_or_handle.split("@")[-1]
            response = (
                self.youtube.channels().list(part="id", forHandle=handle).execute()
            )

        elif "/c/" in channel_url_or_handle:
            custom_name = channel_url_or_handle.split("/c/")[-1]
            response = (
                self.youtube.channels()
                .list(part="id", forUsername=custom_name)
                .execute()
            )

        elif "/channel/" in channel_url_or_handle:
            return channel_url_or_handle.split("/channel/")[-1]

        return response["items"][0]["id"] if response["items"] else None
