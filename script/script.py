from .scraper.streeteasy import StreetEasyScraper
from .scraper.zillow import ZillowScraper


# streeteasy_scraper = StreetEasyScraper()

# streeteasy_scraper.get_borough_listings("Brooklyn")


zillow_scraper = ZillowScraper()

listings = zillow_scraper.get_borough_listings("Brooklyn")

for listing in listings:
    print(listing.get("url"), listing.get("date"), listing.get("status"))
    break
