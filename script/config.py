from dotenv import load_dotenv
import os


load_dotenv()


APIFY_KEY = os.getenv("APIFY_KEY")
STREETEASY_ACTOR_ID = os.getenv("STREETEASY_ACTOR_ID")
ZILLOW_ACTOR_ID = os.getenv("ZILLOW_ACTOR_ID")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
