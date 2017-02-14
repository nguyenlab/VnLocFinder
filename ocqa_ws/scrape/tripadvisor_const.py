__author__ = 'danilo@jaist.ac.jp'

MAIN_URL = "http://www.tripadvisor.com/"

GPS_RGX = r"&center=(?P<lat>\d+\.\d+),(?P<lon>\d+\.\d+)&"

TA_HOME_XPATH = {
    "LOCATION_INPUT_ID": "GEO_SCOPED_SEARCH_INPUT",
    "LOCATION_BOX": "//div[@id='GEO_SCOPE_CONTAINER']/div",
    "LOCATION_SEL": "//div[@id='GEO_SCOPE_CONTAINER']/div/ul/li",
    "QUERY_INPUT_ID": "mainSearch",
    "QUERY_SUBMIT_ID": "SEARCH_BUTTON"
}

TA_COMMON_XPATH = {
    "AD_CLOSE_BUTTON1": "//div[@class='xCloseGreen track_target_x']",
    "AD_CLOSE_BUTTON2": "//div[@class='close']",
    "PAGENUMS": "//div[@class='pageNumbers']/a[contains(@class, 'pageNum')]",
    "PAGENUM_LINK_1": "//div[@class='pageNumbers']/a[contains(@class, 'pageNum') and @data-page-number='%s']",
    "PAGENUM_LINK_2": "//div[@class='pgLinks']//a[contains(@class, 'paging') and text()='%s']"
}

TA_QUERY_XPATH_FREEFORM = {
    "RESULTS": "//div[contains(@class, 'result')]",
    "CATEGORY": ".//div[@class='thumbnail']/div[@class='type']/span",
    "PICTURE_URL": "./div[@class='thumbnail']//img[@class='photo_image']",
    "TITLE": ".//div[contains(@class, 'info poi-info')]/div[@class='title']/span",
    "TITLE_LINK": ".//div[contains(@class, 'info poi-info')]/div[@class='title']",
    "REVIEW_SUMMARY": ".//div[contains(@class, 'info poi-info')]/div[@class='reviews']//span[contains(@class, 'rate')]",
    "ADDRESS": ".//div[contains(@class, 'info poi-info')]/div[@class='address']",
    "TAGCOLL": ".//div[contains(@class, 'info poi-info')]/div[@class='tags']",
    "TAG": "./div[@class='tag']"
}

TA_QUERY_XPATH_RESTAURANT = {
    "RESULTS": "//div[contains(@class, 'listing')]",
    "PICTURE_URL": "./div[@class='photo_booking ']//img[@class='photo_image']",
    "TITLE": "./div[contains(@class, 'shortSellDetails')]/h3[@class='title']/a",
    "REVIEW_SUMMARY": "./div[contains(@class, 'shortSellDetails')]/div[@class='rating']/span[contains(@class, 'rate')]",
    "TAGCOLL": "./div[contains(@class, 'shortSellDetails')]/div[contains(@class, 'cuisines')]",
    "TAG": "./a[@class='cuisine']"
}

TA_DETAIL_XPATH = {
    "ADDRESS": "//span[@class='format_address']",
    "PHONE_NUM": "//div[@class='fl phoneNumber']",
    "LOCATION": "//span[@class='mapWxH']/img[contains(@src, 'maps.google.com')]",
    "REVIEWS": "//div[@id='REVIEWS']",
    "REVIEW_BOX": ".//div[@class='innerBubble']",
    "REVIEW_TITLE": ".//span[@class='noQuotes']",
    "REVIEW_TEXT": ".//p[@class='partial_entry']",
    "REVIEW_SCORE": ".//img[contains(@class, 'sprite-rating_s_fill rating_s_fill')]",
    "NATIVE_NAME": "//span[@class='localNameValue']",
    "NATIVE_ADDRESS": "//span[@class='localAddressValue']"
}