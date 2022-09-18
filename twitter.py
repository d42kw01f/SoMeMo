try:
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import NoSuchElementException
    import argparse
    import time
    import csv
    from fake_headers import Headers
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.firefox import GeckoDriverManager
    import json
except ModuleNotFoundError:
    print("\t<< Please download dependencies from requirement.txt")
except Exception as ex:
    print(ex)

def scroll_down(driver,pageNum):
    print('\n>>>>>>>>>>>>>>>>>> scrolling down to the page # ', pageNum)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

def __scroll_down_page(driver, speed, current_scroll_position):
    new_height= current_scroll_position + 1
    goinDown = 0
    print('current', current_scroll_position)
    while True:
        current_scroll_position += speed
        driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
        new_height = driver.execute_script("return document.body.scrollHeight")
        goinDown += 1
        print(goinDown)
        if goinDown == 200:
            print('this is new height', new_height)
            return new_height


def scraping(driver, pages):
    new_position1 = 0
    for _ in range(0, pages):
        print('Comes here', pages)
        new_position = __scroll_down_page(driver=driver, speed=8, current_scroll_position=new_position1)
        new_position1 = new_position
        print('out side scroll function', new_position, type(new_position))
        tweets = driver.find_elements_by_css_selector("article[data-testid='tweet']")

        print(f'\n>> Found {len(tweets)} tweets.')
        NumTweet = 0
        for tweet in tweets:
            try:
                username_element = tweet.find_element_by_css_selector("div[data-testid='User-Names']")
                username = username_element.find_element_by_tag_name('a').get_attribute('href')
            except:
                username = 'NA'
            try:
                content = tweet.find_element_by_css_selector("div[data-testid='tweetText']")
                content = content.text
            except:
                content = 'NA'
            try:
                date = tweet.find_element_by_tag_name("time").get_attribute('datetime')
            except:
                date = 'NA'
            try:
                likes = tweet.find_element_by_css_selector("div[data-testid='like']").get_attribute('aria-label').split(' ')[0]
            except:
                likes = 'NA'
            try:
                comments = tweet.find_element_by_css_selector("div[data-testid='reply']").get_attribute('aria-label').split(' ')[0]
            except:
                comments = 'NA'
            try:
                shares = tweet.find_element_by_css_selector("div[data-testid='retweet']").get_attribute('aria-label').split(' ')[0]
            except:
                shares = 'NA'
            NumTweet += 1
            print('----', NumTweet)
            print('$ date', date)
            print('$ likes ', likes)
            print('$ comments ', comments)
            print('$ shares ', shares)
            print('$ username ', username)
            print('$ content|text ', content)
            print('\n------------------------------------------------\n')
            with open("/home/unknown/SocialMediaMonitoring/Hashtag/Twitter/outputs/twitter_hashtags.csv", 'a') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([content, date, likes, comments, shares, username])

def main():
    # Settting up the driver
    driver = webdriver.Firefox(executable_path=r'/usr/bin/geckodriver')
    URL = "https://twitter.com/hashtag/Sri Lanka"
    driver.get(URL)
    wait = WebDriverWait(driver, 160) 

    # Waiting until the page loads
    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "article[data-testid='tweet']")))
    print('>>>>>>>>>>>>>>>>>> succesfully, loaded the page\n')
    scraping(driver=driver, pages=20)

    # Closing the driver
    driver.close()
    driver.quit()

main()
