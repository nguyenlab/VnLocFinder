__author__ = 'danilo@jaist.ac.jp'

from dal.db import QAStore
from qa_model import OrganizationPlaceAnswer
from scrape.tripadvisor_scrape import TAScraper


def main():
    scraper = TAScraper()
    store = QAStore()

    fmisspic = open("img_list")

    for line in fmisspic:
        ans = store.get_answers({"uid": line.strip()})[0]

        restaurant = OrganizationPlaceAnswer()
        restaurant.from_dict(ans)
        scraper.collect_picture_restaurant(restaurant)
        print restaurant.to_dict()

    fmisspic.close()


if __name__ == "__main__":
    main()