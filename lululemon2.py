from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import csv
import re


driver = webdriver.Chrome()

driver.get("https://shop.lululemon.com/c/men/run/_/N-1z141cpZ7tu?icid=US;mensrun360landing;hero;video;CTA;MayWk3;shopmensrun")

### Initiate scrolling ###
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)
print("At the bottom")

### Create csv file ###
csv_file = open('lululemon2.csv', 'w')
writer = csv.writer(csv_file)

### Find all href's for eachproduct on results page ###
product_urls = [i.get_attribute('href') for i in driver.find_elements_by_xpath('.//div[@class="product-display-name"]//a')]
product_urls = [x for x in product_urls if "shoes" not in x] ## Shoes not by lululemon
product_index = 1 ## Keep track of what product we are on

### Loop through each product's URL ###
for item in product_urls[:30]:
    driver.get(item)
    time.sleep(5)

    print('Scraping product #' + str(product_index)) ## Which product # we are on
    print('='*50)
    product_index = product_index + 1

    ### Get all reviews on page ###
    reviews = driver.find_elements_by_xpath("//*[contains(@id, 'BVRRDisplayContentReviewID_')]")

    print('There are a total of ' + str(len(reviews)) + ' reviews for this page.')
    print('='*50)

    ### Find total amount of reviews
    # reviews_total = driver.find_element_by_xpath('.//span[@class="reviews-count"]').text
    # reviews_total = reviews_total.rstrip()
    # reviews_total = reviews_total.lstrip()
    # print(reviews_total)
    # print(type(reviews_total))
    # if int(reviews_total) <= 8:
    #     pages_reviews = 1
    # elif ((int(reviews_total) - 8) % 30) == 0:
    #     pages_reviews = 1 + (int(reviews_total) / 30)
    # else:
    #     pages_reviews = 1 + (int(reviews_total) // 30 + 1)
    #
    # print('There are a total of ' + str(pages_reviews) + ' pages of reviews')

    review_index = 1 ## Keep track of what review we are on
    review_page_index = 1 ## Keep track of what review page we are pn

    print("On review page #" + str(review_page_index))
    print('_'*50)
    review_page_index = review_page_index + 1

    ### Loop through each review on product page ###
    for review in reviews:
        print('Scraping review #' + str(review_index)) ## Which review we are on
        review_index = review_index + 1

        # Create empty dictionary to be filled by customer review details ##
        review_dict = {}
        product = driver.find_elements_by_xpath('.//h1[@class="pdp-title"]')
        product = [i.text for i in product]
        product = product[0]
        print(product)

        ### Handle products that are on sale ###
        # _________________________________________________________________________________ #
        try:
            status = driver.find_element_by_xpath('.//span[@class=pdp-flag"]/span').text
        except NoSuchElementException:
            status = ""

        try:
            sale_price = driver.find_element_by_xpath('.//span[@class="sale-price"]').text
        except NoSuchElementException:
            sale_price = ""
        # _________________________________________________________________________________ #

        title = review.find_element_by_xpath('.//span[@class="BVRRValue BVRRReviewTitle"]').text

        ### Catch fields that are not present in user details ###

        # ------------- Fill reviews dictionary -------------- #

        ### Product details ###
        review_dict['product'] = product
        review_dict['status'] = status
        review_dict['sale_price'] = sale_price


        ### User review details ###
        review_dict['title'] = title

        writer.writerow(review_dict.values())

        print('Title of review: ' + review_dict['title'])
        print('Product: ' + review_dict['product'])
        print('Status: ' + review_dict['status'])
        print('Sale Price: ' + review_dict['sale_price'])
        print('_'*50)
        print('I am over this set of reviews--moving on to the next review :)')
        print('='*50) ## Scrape user details and review content

    ### Locate the next button on the page ###

    try:
        next_button = driver.find_element_by_xpath('//a[@name="BV_TrackingTag_Review_Display_NextPage"]')
        print('Going to next page of reviews.')
        next_button.click()
        time.sleep(5)
        reviews = driver.find_elements_by_xpath("//*[contains(@id, 'BVRRDisplayContentReviewID_')]")

        for review in reviews:
            print('Scraping review #' + str(review_index)) ## Which review we are on
            review_index = review_index + 1

            ## Create empty dictionary to be filled by customer review details ##
            review_dict = {}

            product = driver.find_elements_by_xpath('.//h1[@class="pdp-title"]')
            product = [i.text for i in product]
            product = product[0]
            print(product)
            try:
                status = driver.find_element_by_xpath('//.h1[@class=pdp-title"]/span').text
            except NoSuchElementException:
                status = ""

            try:
                sale_price = driver.find_element_by_xpath('.//span[@class="sale-price"]').text
            except NoSuchElementException:
                sale_price = ""
            ### Find all user details ###
            title = review.find_element_by_xpath('.//span[@class="BVRRValue BVRRReviewTitle"]').text
            # ------------- Fill reviews dictionary -------------- #

            review_dict['product'] = product
            review_dict['status'] = status
            review_dict['sale_price'] = sale_price


            ### User review details ###
            review_dict['title'] = title

            writer.writerow(review_dict.values())

            print('Title of review: ' + review_dict['title'])
            print('Product: ' + review_dict['product'])
            print('Status: ' + review_dict['status'])
            print('Sale Price: ' + review_dict['sale_price'])
            print('_'*50)
            print('I am over this set of reviews--moving on to the next review :)')
            print('='*50) ## Scrape user details and review content
    except NoSuchElementException:
        print('Bye now!')
    try:
        next_button = driver.find_element_by_xpath('//a[@name="BV_TrackingTag_Review_Display_NextPage"]')
        print('Going to next page of reviews.')
        next_button.click()
        time.sleep(5)
        reviews = driver.find_elements_by_xpath("//*[contains(@id, 'BVRRDisplayContentReviewID_')]")

        for review in reviews:
            print('Scraping review #' + str(review_index)) ## Which review we are on
            review_index = review_index + 1

            ## Create empty dictionary to be filled by customer review details ##
            review_dict = {}
            product = driver.find_elements_by_xpath('.//h1[@class="pdp-title"]')
            product = [i.text for i in product]
            product = product[0]
            print(product)

            try:
                status = driver.find_element_by_xpath('.//h1[@class=pdp-title"]/span').text
            except NoSuchElementException:
                status = ""

            try:
                sale_price = driver.find_element_by_xpath('//span[@class="sale-price"]').text
            except NoSuchElementException:
                sale_price = ""
            # _________________________________________________________________________________ #
            title = review.find_element_by_xpath('.//span[@class="BVRRValue BVRRReviewTitle"]').text
            # ------------- Fill reviews dictionary -------------- #

            ### Product details ###
            review_dict['product'] = product
            review_dict['status'] = status
            review_dict['sale_price'] = sale_price


            ### User review details ###
            review_dict['title'] = title

            writer.writerow(review_dict.values())

            print('Title of review: ' + review_dict['title'])
            print('Product: ' + review_dict['product'])
            print('Status: ' + review_dict['status'])
            print('Sale Price: ' + review_dict['sale_price'])
            print('_'*50)
            print('I am over this set of reviews--moving on to the next review :)')
            print('='*50) ## Scrape user details and review content
    except NoSuchElementException:
        print('Bye now!')
