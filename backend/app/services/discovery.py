from apify_client import ApifyClient

from app.core.config import settings


class DiscoveryService:
    @staticmethod
    def discover(title: str, location: str, limit: int = 20) -> list[dict]:
        """Trigger Apify actor and return raw job listings."""
        client = ApifyClient(settings.APIFY_API_TOKEN)
        run = client.actor(settings.APIFY_ACTOR_ID).call(
            run_input={
                "queries": [f"{title} {location}"],
                "limit": limit,
            }
        )
        items = client.dataset(run["defaultDatasetId"]).list_items().items
        return [
            {
                "title": item.get("title", ""),
                "company": item.get("company", item.get("companyName", "")),
                "description": item.get("description", item.get("descriptionText", "")),
                "url": item.get("url", item.get("jobUrl", "")),
            }
            for item in items
        ]
