import requests
import re
from bs4 import BeautifulSoup

# Define base url
BASE_URL = "https://www.amazon.co.uk/"
# User agent for http requests
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0"


def check_url(url):
    """
    Does some basic checks to see if url is an amazon url based on base url. Then tries to shorten the url
    by finding the asin based on index of '/dp/' or '/gp/' in the url passed in
    :param url: Amazon url of product that is to be checked
    :return: If all checks go well, a shortened url will be passed out, else None will be passed
    """
    # Check if url contains base url
    if BASE_URL in url:
        # Look for '/dp/' in url
        dp_ind = url.find("/dp/")
        if dp_ind != -1:
            # If found, look for the '/ref'
            ref_ind = url.find("/ref")
            if ref_ind != -1:
                # if found we now have start and end indexes to extract asin
                return BASE_URL + url[dp_ind:ref_ind], "Success"
        # If '/dp/' not found look for '/gp/' instead
        else:
            gp_ind = url.find("/gp/")
            if gp_ind != -1:
                ref_ind = url.find("/ref")
                if ref_ind != -1:
                    return BASE_URL + url[dp_ind:ref_ind], "Success"
            else:
                # If '/gp/' isnt found either, return None
                return None, "/gp/ not found in url"
    else:
        # Return None if not an Amazon url
        return None, "Not a valid Amazon url"


def price_to_float(price):
    """
    Takes a price string and removes formatting. Returns float
    :param price: string price extracted from Amazon product page
    :return: Float of the price value
    """

    # Use regular expressions to find the price value, return a float
    return float(re.sub(r"[^\d.]", "", price))


def get_product_details(url):
    """
    Get product information from the Amazon product page.
    Information includes: title, price, deal status, and the shortened url
    :param url: Amazon product url
    :return: details dictionary
    """

    # Define headers for http request
    headers = {"User-Agent": USER_AGENT}
    # Define the structure of product details
    details = {"title": "", "price": 0, "deal": True, "url": ""}
    # Init result
    result = "Success"
    # Check url
    url_check = check_url(url)
    # Return None if url checks failed
    if url_check[0] is None:
        details = None
        result = url_check[1]

    else:
        url = url_check[0]
        # Get request on url
        page = requests.get(url, headers=headers)
        # Check request was successful
        if page.status_code == 200:
            # Parse page content using bs4
            soup = BeautifulSoup(page.content, "html5lib")
            # Get product title
            title = soup.find(id="productTitle")
            # Get Product price from the deal block
            price = soup.find(id="priceblock_dealprice")
            # If no price is found here we can assume that there is no deal atm
            if price is None:
                price = soup.find(id="priceblock_ourprice")
                details["deal"] = False
            # If title and price not found return None
            if title is not None and price is not None:
                details["title"] = title.get_text().strip()
                details["price"] = price_to_float(price.get_text())
                details["url"] = url
            else:
                details = None
                result = "Details not found."
        else:
            details = None
            result = "Get request status not 200."

    return details, result


if __name__ == "__main__":

    print(get_product_details("https://www.amazon.co.uk/Sennheiser-Special-Open-Headphone-Black/dp/B07Q7S7247/ref=sr_1_3?dchild=1&keywords=hd+599&qid=1599728882&sr=8-3"))