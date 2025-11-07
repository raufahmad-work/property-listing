from .config import STREETEASY_ACTOR_LIMIT, ZILLOW_ACTOR_LIMIT


STREET_BASE_INPUT = {
            "limit": int(STREETEASY_ACTOR_LIMIT),
            "query": ["borough"],
        }

ZILLOW_BASE_INPUT = {
            "amenities:approvedVirtualTour": False,
            "amenities:areApplicationsAccepted": False,
            "amenities:areUtilitiesIncluded": False,
            "amenities:cats": False,
            "amenities:controlledAccess": False,
            "amenities:elevatorAccess": False,
            "amenities:furnished": False,
            "amenities:garage": False,
            "amenities:hasDisabledAccess": False,
            "amenities:hasHardwoodFloor": False,
            "amenities:haveAirConditioning": False,
            "amenities:havePool": False,
            "amenities:highSpeedInternetAvailable": False,
            "amenities:incomeRestricted": False,
            "amenities:isFeaturedListing": False,
            "amenities:largeDogs": False,
            "amenities:laundryAvailable": False,
            "amenities:noPetsAllowed": False,
            "amenities:onWaterfront": False,
            "amenities:openHouses": False,
            "amenities:outdoorSpace": False,
            "amenities:parkingAvailable": False,
            "amenities:shortTermLease": False,
            "amenities:showCase": False,
            "amenities:singleStory": False,
            "amenities:smallDogs": False,
            "dev_dataset_clear": False,
            "dev_no_strip": False,
            "filters:priceReduction": False,
            "includes:attributionInfo": False,
            "includes:description": False,
            "includes:foreClosure": False,
            "includes:homeInsights": False,
            "includes:localProtections": False,
            "includes:priceHistory": False,
            "includes:resoFacts": False,
            "includes:schools": False,
            "includes:taxHistory": False,
            "includes:tourEligibility": False,
            "includes:walkScores": False,
            "limit": int(ZILLOW_ACTOR_LIMIT),
            "map_viewer": False,
            "no_hoa": False,
            "noboundary": False,
            "scanonly": False,
            "show_no_hoa": False
        }

SOURCE_CHOICES = ("zillow", "streeteasy")
BOROUGH_CHOICES = ("Brooklyn", "Bronx", "Manhattan", "Queens", "Staten Island")
