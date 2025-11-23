"""Wikipedia API client for searching and retrieving articles."""
import httpx
from typing import Optional, Dict, Any, List
from datetime import datetime


class WikipediaClient:
    """Client for Wikipedia API."""

    BASE_URL = "https://en.wikipedia.org/api/rest_v1"
    SEARCH_URL = "https://en.wikipedia.org/w/api.php"

    def __init__(self, language: str = "en"):
        """Initialize Wikipedia client.

        Args:
            language: Wikipedia language code (default: en)
        """
        self.language = language
        if language != "en":
            self.BASE_URL = f"https://{language}.wikipedia.org/api/rest_v1"
            self.SEARCH_URL = f"https://{language}.wikipedia.org/w/api.php"

    def search(self, keyword: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search Wikipedia for articles.

        Args:
            keyword: Search keyword
            limit: Maximum number of results

        Returns:
            List of search results with title and pageid
        """
        params = {
            "action": "query",
            "list": "search",
            "srsearch": keyword,
            "srlimit": limit,
            "format": "json"
        }

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.get(self.SEARCH_URL, params=params)
                response.raise_for_status()
                data = response.json()

                results = []
                for item in data.get("query", {}).get("search", []):
                    results.append({
                        "title": item.get("title", ""),
                        "pageid": item.get("pageid", 0),
                        "snippet": item.get("snippet", "")
                    })
                return results
        except Exception as e:
            print(f"Error searching Wikipedia: {e}")
            return []

    def get_summary(self, title: str) -> Optional[Dict[str, Any]]:
        """Get article summary.

        Args:
            title: Article title

        Returns:
            Dictionary with title, summary, url, and timestamp
        """
        try:
            # URL encode the title
            encoded_title = title.replace(" ", "_")
            url = f"{self.BASE_URL}/page/summary/{encoded_title}"

            with httpx.Client(timeout=30.0) as client:
                response = client.get(url)
                response.raise_for_status()
                data = response.json()

                return {
                    "title": data.get("title", title),
                    "summary": data.get("extract", ""),
                    "url": data.get("content_urls", {}).get("desktop", {}).get("page", ""),
                    "description": data.get("description", ""),
                    "timestamp": datetime.now().isoformat()
                }
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                print(f"Wikipedia article not found: {title}")
            else:
                print(f"HTTP error getting Wikipedia summary: {e}")
            return None
        except Exception as e:
            print(f"Error getting Wikipedia summary: {e}")
            return None

    def search_and_get_summary(self, keyword: str) -> Optional[Dict[str, Any]]:
        """Search for a keyword and get the summary of the top result.

        Args:
            keyword: Search keyword

        Returns:
            Dictionary with keyword, title, summary, url, and searched_at
        """
        search_results = self.search(keyword, limit=1)
        if not search_results:
            return None

        top_result = search_results[0]
        summary = self.get_summary(top_result["title"])

        if summary:
            return {
                "keyword": keyword,
                "title": summary["title"],
                "summary": summary["summary"],
                "url": summary["url"],
                "description": summary.get("description", ""),
                "searched_at": summary["timestamp"]
            }
        return None
