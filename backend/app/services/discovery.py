from urllib.parse import quote_plus

from apify_client import ApifyClient

from app.core.config import settings


class DiscoveryService:
    @staticmethod
    def discover(title: str, location: str, limit: int = 20) -> list[dict]:
        """Trigger Apify actor and return raw job listings."""
        client = ApifyClient(settings.APIFY_API_TOKEN)
        search_url = (
            f"https://www.linkedin.com/jobs/search/"
            f"?keywords={quote_plus(title)}&location={quote_plus(location)}"
        )
        run = client.actor(settings.APIFY_ACTOR_ID).call(
            run_input={
                "urls": [search_url],
                "limit": limit,
            }
        )
        items = client.dataset(run["defaultDatasetId"]).list_items().items
        return [
            {
                "title": item.get("title", ""),
                "company": item.get("companyName", ""),
                "description": item.get("descriptionText", ""),
                "url": item.get("link", ""),
            }
            for item in items
        ]
