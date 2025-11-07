from dotenv import load_dotenv
import os


load_dotenv()


APIFY_API_KEY = os.getenv("APIFY_API_KEY")
STREETEASY_ACTOR_ID = os.getenv("STREETEASY_ACTOR_ID")
ZILLOW_ACTOR_ID = os.getenv("ZILLOW_ACTOR_ID")
STREETEASY_ACTOR_LIMIT = os.getenv("STREETEASY_ACTOR_LIMIT")
ZILLOW_ACTOR_LIMIT = os.getenv("ZILLOW_ACTOR_LIMIT")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
