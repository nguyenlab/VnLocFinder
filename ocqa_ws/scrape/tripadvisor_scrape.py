#!/usr/bin/env python

import sys
import os
import re
import time
import urllib2

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from qa_model import OrganizationPlaceAnswer, CustomerReview, EntType
from scrape.tripadvisor_const import MAIN_URL
from scrape.tripadvisor_const import TA_COMMON_XPATH as TACX, TA_DETAIL_XPATH as TADX
from scrape.tripadvisor_const import TA_HOME_XPATH as TAHX
from scrape.tripadvisor_const import TA_QUERY_XPATH_RESTAURANT as TAQXR
from scrape.tripadvisor_const import GPS_RGX
from dal.db import QAStore


EX_PLACE = "Nomi, Ishikawa prefecture, Japan"
EX_QUERY = "restaurant"
LOCATIONS_URL = "https://www.tripadvisor.com/Restaurants-g294232-Japan.html"

class TAScraper:
    def __init__(self):
        self.driver = webdriver.Firefox()
        #self.driver.set_window_size(1120, 550)
        self.driver.implicitly_wait(0)
        self.store = QAStore()


    def query_ta(self, place, query):
        self.driver.get(MAIN_URL)
        self.close_ad()
        self.driver.switch_to.default_content()
        self.driver.find_element_by_id(TAHX["LOCATION_INPUT_ID"]).clear()
        self.driver.find_element_by_id(TAHX["LOCATION_INPUT_ID"]).send_keys(place)


        location_set = False
        while (not location_set):
            try:
                self.driver.switch_to.window(self.driver.current_window_handle)
                self.driver.find_element_by_xpath(TAHX["LOCATION_BOX"]).text
                location_sel_elem = self.driver.find_element_by_xpath(TAHX["LOCATION_SEL"])
                location_sel_elem.click()
                location_set = True
                self.driver.implicitly_wait(0)
            except (NoSuchElementException):
                self.driver.implicitly_wait(1)
                location_set = False

        self.driver.find_element_by_id(TAHX["QUERY_INPUT_ID"]).click()
        self.driver.find_element_by_id(TAHX["QUERY_INPUT_ID"]).send_keys(query)
        self.driver.find_element_by_id(TAHX["QUERY_SUBMIT_ID"]).click()
        print self.driver.current_url


    def close_ad(self):
        try:
            self.driver.implicitly_wait(0.5)
            try:
                ad_elem = self.driver.find_element_by_xpath(TACX["AD_CLOSE_BUTTON1"])
                ad_elem.click()
            except (NoSuchElementException):
                ad_elem = self.driver.find_element_by_xpath(TACX["AD_CLOSE_BUTTON2"])
                ad_elem.click()
        except (NoSuchElementException):
            pass

        self.driver.implicitly_wait(0)


    def page_loop(self, url, op, data=None):
        self.driver.get(url)
        max_page = 0
        retries = 0
        while (not max_page):
            try:
                pgnums = self.driver.find_elements_by_xpath(TACX["PAGENUMS"])
                max_page = sorted([int(pgnum.get_attribute("data-page-number")) for pgnum in pgnums])[-1]
            except (NoSuchElementException, IndexError):
                print "No page counter: ", self.driver.current_url
                self.close_ad()

                retries += 1
                if (retries > 10):
                    if (data is not None):
                        op(data)
                    else:
                        op()

                    return

        for pgnum in xrange(1, max_page + 1):
            self.close_ad()
            if (data is not None):
                op(data)
            else:
                op()

            if (pgnum < max_page):
                try:
                    page_link = self.driver.find_element_by_xpath(TACX["PAGENUM_LINK_1"] % (pgnum + 1))
                except (NoSuchElementException):
                    page_link = self.driver.find_element_by_xpath(TACX["PAGENUM_LINK_2"] % (pgnum + 1))

                page_link.click()


    def collect_locations(self, locations_ret):
        try:
            loc_name_elems = self.driver.find_elements_by_class_name("geo_name")
            loc_names = [loc_elem.find_element_by_tag_name("a").text.replace("Restaurants", "").strip()
                         for loc_elem in loc_name_elems]
            if (not loc_names):
                raise NoSuchElementException
        except (NoSuchElementException):
            loc_name_elems = self.driver.find_elements_by_xpath("//ul[@class='geoList']/li/a")
            loc_names = [loc_elem.text.replace("restaurants", "").strip()
                         for loc_elem in loc_name_elems]

        print loc_names

        locations_ret.extend(loc_names)


    def collect_data_restaurant(self):
        time.sleep(1)
        results = self.driver.find_elements_by_xpath(TAQXR["RESULTS"])

        for result in results:
            title_elem = result.find_element_by_xpath(TAQXR["TITLE"])
            title = title_elem.text

            restaurant = OrganizationPlaceAnswer()
            restaurant.name = title
            restaurant.uri = title_elem.get_attribute("href")

            if (self.store.exist_answer(restaurant)):
                continue

            try:
                picture_url = result.find_element_by_xpath(TAQXR["PICTURE_URL"]).get_attribute("src")
                picture = urllib2.urlopen(picture_url).read()
                with open("images/" + restaurant.uid + ".jpg", "wb") as picfile:
                    picfile.write(picture)
                picture_url = restaurant.uid + ".jpg"

            except (NoSuchElementException):
                picture_url = ""
                print restaurant.name, ": no picture"

            try:
                review_summary_elem = result.find_element_by_xpath(TAQXR["REVIEW_SUMMARY"])
                review_summary = review_summary_elem.get_attribute("class").split()[-1]
                review_summ_score = float(review_summary[2] + "." + review_summary[3])
            except (NoSuchElementException):
                review_summary = ""
                review_summ_score = None
                print restaurant.name, ": no reviews"

            tags = []
            try:
                tagcoll_elem = result.find_element_by_xpath(TAQXR["TAGCOLL"])
                tags_elem = tagcoll_elem.find_elements_by_xpath(TAQXR["TAG"])

                for tag_elem in tags_elem:
                    tags.append(tag_elem.text)
            except (NoSuchElementException, IndexError):
                print restaurant.name, ": no tags"


            restaurant.keywords.append("restaurant")
            restaurant.keywords.extend(tags)
            restaurant.pictureURL = picture_url

            if (review_summ_score is not None):
                custrev = CustomerReview()
                custrev.score = review_summ_score
                custrev.comments = "OVERALL"
                restaurant.customerReviews.append(custrev)

            self.store.insert_answer(restaurant)


    def collect_details_restaurant(self, restaurant):
        self.driver.get(restaurant.uri)
        
        time.sleep(1)
        self.driver.implicitly_wait(0.5)
        try:
            address = self.driver.find_element_by_xpath(TADX["ADDRESS"]).text
        except (NoSuchElementException):
            address = ""
            print restaurant.name, ": no address"

        try:
            native_name = self.driver.find_element_by_xpath(TADX["NATIVE_NAME"]).get_attribute("textContent")
        except (NoSuchElementException):
            native_name = ""
            print restaurant.name, ": no native name"

        try:
            native_address = self.driver.find_element_by_xpath(TADX["NATIVE_ADDRESS"]).get_attribute("textContent")
        except (NoSuchElementException):
            native_address = ""
            print restaurant.name, ": no native address"

        try:
            location_elem = self.driver.find_element_by_xpath(TADX["LOCATION"])
            location_mo = re.search(GPS_RGX, location_elem.get_attribute("src"))
            location = (float(location_mo.group("lat")), float(location_mo.group("lon")))
        except (NoSuchElementException, AttributeError):
            location = (0.0, 0.0)
            print restaurant.name, ": no location"

        try:
            phone_number = self.driver.find_element_by_xpath(TADX["PHONE_NUM"]).text
        except (NoSuchElementException):
            phone_number = ""
            print restaurant.name, ": no phone number"

        reviews = []
        try:
            reviews_elem = self.driver.find_element_by_xpath(TADX["REVIEWS"])
            for review_elem in reviews_elem.find_elements_by_xpath(TADX["REVIEW_BOX"]):
                review_title = review_elem.find_element_by_xpath(TADX["REVIEW_TITLE"]).text
                review_text = review_elem.find_element_by_xpath(TADX["REVIEW_TEXT"]).text
                review_score_elem = review_elem.find_element_by_xpath(TADX["REVIEW_SCORE"])
                review_score_str = review_score_elem.get_attribute("class").split()[-1]
                review_score = float(review_score_str[1] + "." + review_score_str[2])

                custrev = CustomerReview()
                custrev.score = review_score
                custrev.comments = review_title + "\n\n" + review_text
                reviews.append(custrev)

        except (NoSuchElementException):
            print restaurant.name, ": no reviews"

        restaurant.customerReviews.extend(reviews)
        restaurant.address = address
        restaurant.telephoneNumber = phone_number
        restaurant.gpsPosition = location
        restaurant.nativeName = native_name
        restaurant.nativeAddress = native_address

        self.store.update_answer(restaurant)

        main_window = self.driver.window_handles[0]
        while (len(self.driver.window_handles) > 1):
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.close()
            self.driver.switch_to.window(main_window)


    def collect_picture_restaurant(self, restaurant):
        self.driver.get(restaurant.uri)
        self.driver.implicitly_wait(30)

        try:
            picture_url = self.driver.find_element_by_id("HERO_PHOTO").get_attribute("src")
            picture = urllib2.urlopen(picture_url).read()
            with open("images/" + restaurant.uid + ".jpg", "wb") as picfile:
                picfile.write(picture)

        except (NoSuchElementException):
            print restaurant.name, ": no picture"

        main_window = self.driver.window_handles[0]
        while (len(self.driver.window_handles) > 1):
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.close()
            self.driver.switch_to.window(main_window)


def scraper_task(location):
    scraper = TAScraper()
    place = location + ", " + "Japan"
    query = EX_QUERY

    scraper.query_ta(place, query)
    scraper.page_loop(scraper.driver.current_url, scraper.collect_data_restaurant)

    scraper.store.conn.close()
    main_window = scraper.driver.window_handles[0]
    while (len(scraper.driver.window_handles) > 1):
        scraper.driver.switch_to.window(scraper.driver.window_handles[1])
        scraper.driver.close()
        scraper.driver.switch_to.window(main_window)

    scraper.driver.close()


def fill_area():
    store = QAStore()
    ans_cur = store.get_answers({})

    for ans in ans_cur:
        upd_ans = dict()
        upd_ans["uid"] = ans["uid"]
        area_name = ans["uri"].split("-")[-1].split(".")[0]
        area_name = re.sub(r"_(cho|son|gun|machi|mura|Prefecture)", r" \1", area_name)
        upd_ans["area"] = area_name.split("_")
        store.update_answer(upd_ans)


def fill_details():
    scraper = TAScraper()
    store = QAStore()

    while (True):
        ans_cur = store.get_answers({"address": "",
                                     "entType": EntType.PLACE + EntType.ORGANIZATION,
                                     "name": {"$regex": r"^" + sys.argv[1], "$options": "i"}}).limit(100)

        if (ans_cur.count() == 0):
            break

        for ans in ans_cur:
            restaurant = OrganizationPlaceAnswer()
            restaurant.from_dict(ans)
            scraper.collect_details_restaurant(restaurant)
            print restaurant.to_dict()



def main(argv):
    # try:
    #     locations = cPickle.load(open("locations_jp.pickle"))
    # except IOError:
    #     locations = []
    #     scraper = TAScraper()
    #     scraper.page_loop(LOCATIONS_URL, scraper.collect_locations, locations)
    #     cPickle.dump(locations, open("locations_jp.pickle", "wb"), cPickle.HIGHEST_PROTOCOL)
    #     scraper.driver.close()
    #
    # start = int(argv[1])
    # end = int(argv[2])
    # cur = start
    # for location in locations[start:end]:
    #     scraper_task(location)
    #
    #     print "Progress: ", cur
    #     cur += 1

    fill_details()



if __name__ == "__main__":
    main(sys.argv)
