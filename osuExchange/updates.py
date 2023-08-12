from typing import Optional
from osuExchange.api import get as api_get
from osuExchange.typing import GameMode, JsonObject

class Build:
    class UpdateStream:
        def __init__(self, json: JsonObject):
            display_name: Optional[str] = json.get('display_name')
            id: int = json['id']
            is_featured: bool = json['is_featured']
            name: str = json['name']

    class ChangelogEntry:
        def __init__(self, json: JsonObject):
            category: str = json['category']
            created_at: Optional[str] = json.get('created_at')
            github_pull_request_id: Optional[int] = json.get('github_pull_request_id')
            github_url: Optional[str] = json.get('github_url')
            id: Optional[int] = json.get('id')
            major: bool = json['major']
            repository: Optional[str] = json.get('repository')
            title: Optional[str] = json.get('title')
            type: str = json['type']
            url: Optional[str] = json.get('url')

            # Optional Attributes
            github_user: Optional[Build.GithubUser] = json.get('github_user')
            message: Optional[str] = json.get('message')
            message_html: Optional[str] = json.get('message_html')

    
    class GithubUser:
        def __init__(self, json: JsonObject):
            display_name: str = json['display_name']
            github_url: Optional[str] = json.get('github_url')
            id: Optional[int] = json.get('id')
            osu_username: Optional[str] = json.get('osu_username')
            user_id: Optional[int] = json.get('user_id')
            user_url: Optional[str] = json.get('user_url')
    
    class Versions:
        def __init__(self, json: JsonObject):
            next: Optional[Build] = json.get('next')
            previous: Optional[Build] = json.get('previous')
        

    def __init__(self, json: JsonObject):
        created_at: str = json['created_at']
        display_version: str = json['display_version']
        id: int = json['id']
        update_stream: Optional[Build.UpdateStream] = json.get('update_stream')
        users: int = json['users']
        version: Optional[str] = json.get('version')
        youtube_id: Optional[str] = json.get('youtube_id')

        # Optional
        changelog_entries: Optional[list[Build.ChangelogEntry]] = json.get('changelog_entries')
        versions: Optional[Build.Versions] = json.get('versions')

def get_beatmap_scores(access_token: str, 
        stream: str, 
        build: str
) -> Build:
	return Build(api_get(f'/changelog/{stream}/{build}', access_token).json())
        
        
