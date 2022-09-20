from bs4 import BeautifulSoup
import time
import csv
from facebook_scraper import get_posts


def Scraping(username):
    posts = get_posts('sajithpremadasa', cookies='/home/d42kw01f/Downloads/cookies.json')
    list_posts = list(posts)
    title = []
    comments = []
    shares = []
    date = []
    content = []
    for i in range(2, len(list_posts)):
        try:
            title = ''
            likes = list_posts[i]['likes']
            comments = list_posts[i]['comments']
            shares = list_posts[i]['shares']
            date = list_posts[i]['time']
            url = list_posts[i]['post_url']
            content = list_posts[i]['text']
            username = list_posts[i]['user_url']
            print(date, url, likes, comments, shares, username, content)
            print('----------------------------------------------------------------------------------------------')
            with open(f"/home/d42kw01f/Documents/Projects/RadAnalyzer/raw_data/Aragalaya/facebook_{username}.csv", 'a') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([content, date, url, likes, comments, shares, username])
        except:
            print('issue with {}'.format(i))
            pass
