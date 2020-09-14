import db
import scraper
import visualise


if __name__ == "__main__":

    # TODO: Add checks to see if url file exists

    # Load in all urls from text file
    with open("./urls.txt", 'r') as fid:
        urls = fid.readlines()

    for url in urls:

        # Get details for product
        details = scraper.get_product_details(url)

        # If failed
        if details[0] is None:
            result = url + ":" + details[1]

        # Else insert into db
        else:
            inserted = db.add_product_details(details[0])

            if inserted:
                result = "Success"
            else:
                result = url + " : " + result

        print(result)

    visualise.plot_history()