from .models import Listing, Bid 
from django.db.models import Max


def check_bid(listing, bid_placed):
    """ Checks if bid_placed is greater than the current highest bid of listing.
        Returns True if bid_placed is greater than the current highest bid of listing.
        Returns False if bid_placed is not greater than the current highest bid of listing.
    """
    bids = listing.bids.all()
    highest_bid = bids.aggregate(Max('bid'))
    if bid_placed > highest_bid.get('bid__max'):
        return True
    else:
        return False