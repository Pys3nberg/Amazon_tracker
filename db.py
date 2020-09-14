import datetime
import pymongo

# TODO: Should add more database functionality such as select top/last 1 for a give product
#   or filter between dates


# Connect to local mongodb server and amazon db
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["amazon"]


def add_product_details(details):
    """
    Inserts a new entry for a product.
    :param details: details contains title, price, deal status and url
    :return: Boolean flag if successful
    """

    # Get reference to the products table
    new = db["products"]
    # Get the asin from the url
    asin = details["url"][len(details["url"])-10:len(details["url"])]
    # Add datetime to the details structure
    details["date"] = datetime.datetime.utcnow()
    # Try and insert new record
    try:
        new.update_one(
            {
                "asin": asin
            },
            {
                "$set":
                    {
                        "asin": asin
                    },
                "$push":
                    {
                        "details": details
                    }
            },
            upsert=True
        )
        # Return true on success
        return True

    except Exception as error:
        # Error occured, print error message and return false
        print(error)
        return False


def get_product_history(asin):
    """
    Using the product asin, all details for that product
    :param asin: Product id
    :return: details - contains title, price, deal status
    """
    products = db["products"]
    try:
        find = products.find_one({"asin": asin})
        if find:
            return find
    except Exception as error:
        print(error)
        return None


def get_all_product_details():
    """
    Returns all detail entries for all products
    :return: details - contains title, price, deal status
    """
    products = db["products"]
    try:
        find = products.find()
        if find:
            return find
    except Exception as error:
        print(error)
        return None