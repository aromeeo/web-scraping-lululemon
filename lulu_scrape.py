from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import csv


driver = webdriver.Chrome()

driver.get("https://shop.lululemon.com/c/men/_/N-7tu?mnid=mn;en-US-JSON;men;features;view-all")

### Initiate scrolling ###
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(4)
print("Scrolled to bottom - moving to product pages.")

### Create csv file ###
csv_file = open('all_mens26.csv', 'w')
writer = csv.writer(csv_file)

### Find all href's for eachproduct on results page ###
product_urls = [i.get_attribute('href') for i in driver.find_elements_by_xpath('.//div[@class="product-display-name"]//a')]
product_urls = [x for x in product_urls if "shoes" not in x] ## Shoes not by lululemon
product_index = 1 ## Keep track of what product we are on

### Loop through each product's URL ###
for item in product_urls[26:]:
    driver.get(item)
    try:
        review_button = driver.find_element_by_xpath('//a[@class="reviews"]')
        review_button.click()
    except:
        driver.refresh()
        review_button = driver.find_element_by_xpath('//a[@class="reviews"]')
        review_button.click()
    time.sleep(5)

    # print('Scraping product #' + str(product_index)) ## Which product # we are on
    # print('='*50)
    # product_index = product_index + 1

    # print("On review page #" + str(review_page_index))
    # print('_'*50)
    review_page_index = 1 ## Keep track of what review page we are pn
    product = driver.find_element_by_xpath('//h1[@class="pdp-title"]/div').text

    while True:
        try:
            ### Get all reviews on page and set indices ###
            reviews = driver.find_elements_by_xpath("//*[contains(@id, 'BVRRDisplayContentReviewID_')]")
            review_index = 1 ## Keep track of what review we are on


            ### Loop through each review on product page ###
            print('There are a total of ' + str(len(reviews)) + ' reviews for this page.')
            for review in reviews:
                review_index = review_index + 1
                # print('Scraping review #' + str(review_index)) ## Which review we are on


                # Create empty dictionary to be filled by customer review details ##
                review_dict = {}
                product = driver.find_element_by_xpath('//h1[@class="pdp-title"]/div').text
                list_price = driver.find_element_by_xpath('.//span[@class="list-price"]').text
                # _________________________________________________________________________________ #

                average_rating = driver.find_element_by_xpath('.//div[@id="BVRRQuickTakeContentContainerID"]//img').get_attribute('alt')

                ### Catch fields that are not present in user details ###
                try:
                    location = review.find_element_by_xpath('.//span[@class="BVRRValue BVRRUserLocation"]').text
                except NoSuchElementException:
                    location = ""
                try:
                    athleticType = review.find_element_by_xpath('.//span[@class="BVRRValue BVRRContextDataValue BVRRContextDataValueActivity"]').text
                except NoSuchElementException:
                    athleticType = ""
                try:
                    ageRange = review.find_element_by_xpath('.//span[@class="BVRRValue BVRRContextDataValue BVRRContextDataValueAge"]').text
                except NoSuchElementException:
                    ageRange = ""
                try:
                    bodyType = review.find_element_by_xpath('.//span[@class="BVRRValue BVRRContextDataValue BVRRContextDataValueBodyType"]').text
                except NoSuchElementException:
                    bodyType = ""
                try:
                    like = review.find_element_by_xpath('.//div[@class="BVRRTagDimensionContainer BVRRProTagDimensionContainer"]//span[@class="BVRRValue BVRRTags"]').text
                except NoSuchElementException:
                    like = ""
                try:
                    not_like = review.find_element_by_xpath('.//div[@class="BVRRTagDimensionContainer BVRRConTagDimensionContainer"]//span[@class="BVRRValue BVRRTags"]').text
                except NoSuchElementException:
                    not_like = ""
                try:
                    fit = review.find_element_by_xpath('.//div[@class="BVRRRatingSliderImage"]/img').get_attribute('title')
                except NoSuchElementException:
                    fit = ""

                ### Find all user details ###
                user = review.find_element_by_xpath('.//span[@itemprop="author"]').text
                user_rating = review.find_element_by_xpath('.//div[@id="BVSubmissionPopupContainer"]//div[@class="BVRRRatingNormalImage"]/img').get_attribute('title')

                ### Find all user review details ###
                datePublished = review.find_element_by_xpath('.//meta[@itemprop="datePublished"]').get_attribute('content')
                title = review.find_element_by_xpath('.//span[@class="BVRRValue BVRRReviewTitle"]').text
                text = review.find_element_by_xpath('.//span[@class="BVRRReviewText"]').text

                ### Catch fields that are not present in review details ###
                try:
                    responseDate = review.find_element_by_xpath('.//span[@class="BVRRReviewClientResponseSubtitleDate"]').text
                except NoSuchElementException:
                    responseDate = ""
                try:
                    response = review.find_element_by_xpath('.//div[@class="BVRRReviewClientResponseText"]').text
                except NoSuchElementException:
                    response = ""

                ### Find if review was helpful or not ###
                # helpfulYes = review.find_element_by_xpath('//*[@id="BVSubmissionPopupContainer"]/div[4]/div[2]/div[1]/div[3]/span[2]/a/span/span[2]').text
                # helpfulNo = review.find_element_by_xpath('//*[@id="BVSubmissionPopupContainer"]/div[4]/div[2]/div[1]/div[3]/span[3]/a/span/span[2]').text


                # ------------- Fill reviews dictionary -------------- #

                ### Product details ###
                review_dict['product'] = product
                review_dict['list_price'] = list_price
                review_dict['average_rating'] = average_rating

                ### User details ###
                review_dict['user_rating'] = user_rating
                review_dict['user'] = user
                review_dict['location'] = location
                review_dict['athleticType'] = athleticType
                review_dict['ageRange'] = ageRange
                review_dict['bodyType'] = bodyType
                review_dict['like'] = like
                review_dict['not_like'] = not_like
                review_dict['fit'] = fit

                ### User review details ###
                review_dict['title'] = title
                review_dict['datePublished'] = datePublished
                review_dict['text'] = text
                review_dict['responseDate'] = responseDate
                review_dict['response'] = response
                # review_dict['helpfulYes'] = helpfulYes
                # review_dict['helpfulNo'] = helpfulNo
                # _____________________________________________________#

                writer.writerow(review_dict.values())
                print('_'*50)
                print('Product: '+ review_dict['product'])
                print('Title of review: ' + review_dict['title'])
                # print('Helpful:' + [i.text for i in review_dict['helpfulYes']])
                print('_'*50)
                print('I am over this set of reviews--moving on to the next review :)')

            ### Locate the next button on the page ###
            next_button = driver.find_element_by_xpath('//a[@name="BV_TrackingTag_Review_Display_NextPage"]')
            print('Going to next page of reviews.')
            next_button.click()
            review_page_index = review_page_index + 1
            time.sleep(5)

        except NoSuchElementException:
            print('one product done now!')
            break
