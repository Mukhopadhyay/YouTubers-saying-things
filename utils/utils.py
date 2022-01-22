from typing import List
from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id: str, **kwargs) -> List[dict]:
    transcript = YouTubeTranscriptApi.get_transcript(video_id, **kwargs)
    return transcript
