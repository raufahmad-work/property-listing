import os
import glob
from collections import defaultdict
from datetime import datetime

from .config import TO_EMAIL
from .scraper.streeteasy import StreetEasyScraper
from .scraper.zillow import ZillowScraper
from .helpers import create_file, send_email, filter_new_listings, create_records_in_db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)


streeteasy_scraper = StreetEasyScraper()
zillow_scraper = ZillowScraper()
boroughs = ["Brooklyn", "Bronx", "Manhattan", "Queens", "Staten Island"]
search_types = ["rent", "sale"]
search_type_mapping = {"rent": "FOR_RENT", "sale": "FOR_SALE"}

for i, b in enumerate(boroughs, start=1):
    print(f"{i}. {b}")

choice = -1
selected_boroughs = boroughs
while choice not in ["", "1", "2", "3", "4", "5"]:
    choice = input("\nEnter your choice (1-5) (Leave empty to continue with all boroughs): ").strip()
    if choice == '':
        break
    elif choice in ["1", "2", "3", "4", "5"]:
        selected_boroughs = [boroughs[int(choice) - 1]]
    else:
        print("Invalid choice. Please enter a number between 1 and 5 or leave empty.")


streeteasy_data = defaultdict(list)
streeteasy_timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
for borough in selected_boroughs:
    for type in search_types:
        items = streeteasy_scraper.get_borough_listings(borough, type)
        listings = [
            {
                "Address": item.get("title"),
                "Type": search_type_mapping.get(type),
                "URL": item.get("url"),
                "Date Listed": item.get("created_at"),
            } for item in items
        ]
        listings = filter_new_listings(listings)
        streeteasy_data[borough].extend(listings)


create_file(streeteasy_data, f"streeteasy_{streeteasy_timestamp}")



zillow_data = defaultdict(list)
zillow_timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
for borough in selected_boroughs:
    for type in search_types:
        items = zillow_scraper.get_borough_listings(borough, type)
        listings = [
            {
                "Address": item.get("abbreviatedAddress"),
                "Type": item.get("homeStatus"),
                "URL": item.get("url"),
                "Date Listed": item.get("datePostedString"),
            } for item in items
        ]
        listings = filter_new_listings(listings)
        zillow_data[borough].extend(listings)

create_file(zillow_data, f"zillow_{zillow_timestamp}")


file_names = [f"streeteasy_{streeteasy_timestamp}", f"zillow_{zillow_timestamp}"]
file_paths = [os.path.join(PARENT_DIR, f"{file_names[0]}.xlsx"), os.path.join(PARENT_DIR, f"{file_names[1]}.xlsx")]
send_email(file_paths, file_names, TO_EMAIL)


create_records_in_db(streeteasy_data)
create_records_in_db(zillow_data)


for file in glob.glob("*.xlsx"):
    os.remove(file)
