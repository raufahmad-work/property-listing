from apify_client import ApifyClient
from script.config import APIFY_KEY, ZILLOW_ACTOR_ID


class ZillowScraper:
    def __init__(self):
        self.actor_id = ZILLOW_ACTOR_ID
        self.client = ApifyClient(APIFY_KEY)
        self.base_input = {
            "limit": 5,
        }

    def get_borough_listings(self, borough, search_type):
        location = [borough]
        self.base_input["location"] = location
        self.base_input["search_type"] = search_type
        run = self.client.actor(self.actor_id).call(run_input=self.base_input)
        items = self.client.dataset(run["defaultDatasetId"]).iterate_items()
        return items
