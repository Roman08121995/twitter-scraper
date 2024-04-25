from selenium import webdriver
from selenium.webdriver.common.by import By as by
from time import sleep
from parsel import Selector
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import sys
from credentials import my_password, my_handle_name, my_user_email, my_registered_number

import re

def extract_tweet_id(url):
    pattern = r'(?:https?://)?twitter\.com/\w+/status/(\d+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None

def get_driver_chrome():
    """
    The function `get_driver_chrome` sets up a Chrome WebDriver with specific user agent and browser
    options.
    :return: The function `get_driver_chrome()` returns a Chrome WebDriver instance configured with
    specific user agent, options, and settings for automated browsing.
    """
    user_agent = "Mozilla/5.0 (X11; CrOS x86_64 10066.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    options = webdriver.ChromeOptions()
    # options.add_argument(r'user-data-dir=C:\Users\Mubashir Ali\AppData\Local\Google\Chrome\User Data')
    # options.add_argument(r'profile-directory=Profile 3')
    options.add_argument(f"user-agent={user_agent}")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(
        options=options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    return driver

def save_to_csv(data, filename):
    """
    The function `save_to_csv` takes data and a filename as input, appends the data to an existing CSV
    file if it exists, or creates a new CSV file if it doesn't, and saves the data to the CSV file.
    
    :param data: The `data` parameter is the information that you want to save to a CSV file. It could
    be in the form of a dictionary, list of dictionaries, list of lists, or any other suitable data
    structure that can be converted to a DataFrame
    :param filename: The `filename` parameter in the `save_to_csv` function is the name of the CSV file
    where the data will be saved
    """
    df = pd.DataFrame([data])
    if os.path.exists(filename):
        existing_df = pd.read_csv(filename).fillna("")
        df = pd.concat([existing_df, df], ignore_index=True)
    df.to_csv(filename, index=False)


def login(driver):
    """
    The `login` function automates the login process on Twitter using Selenium WebDriver in Python.
    
    :param driver: The `driver` parameter in the `login` function is typically an instance of a web
    driver, such as Selenium WebDriver, that allows you to automate interactions with a web browser. In
    this case, it seems like the function is using the driver to automate the login process on Twitter
    by entering the username
    """
    driver.get("https://twitter.com/i/flow/login")
    sleep(10)
    driver.find_element(by.XPATH,'//input[@autocomplete="username"]').send_keys(my_user_email)
    sleep(1.5)
    driver.find_element(by.XPATH,'//span[text()="Next"]').click()
    sleep(1.5)
    try:
        driver.find_element(by.XPATH,'//input[@data-testid="ocfEnterTextTextInput"]').send_keys(my_handle_name)
        sleep(1.5)
        driver.find_element(by.XPATH,'//span[text()="Next"]').click()
        sleep(1.5)
    except:
        pass
    sleep(1.5)
    driver.find_element(by.XPATH,'//input[@autocomplete="current-password"]').send_keys(my_password)
    sleep(1.5)
    driver.find_element(by.XPATH,'//span[text()="Log in"]').click()
    sleep(20)
    try:
        driver.find_element(by.XPATH,'//input[@autocomplete="tel"]').send_keys(my_registered_number)
        sleep(1.5)
        driver.find_element(by.XPATH,'//span[text()="Next"]').click()
        sleep(10)
    except:
        pass

def get_name_username(article):
    """
    This function extracts the name and username from a given article using XPath.
    
    :param article: The function `get_name_username` takes an article as input and extracts the name and
    username from the article using XPath. The XPath expression selects text within `<span>` elements
    inside a `<div>` element with the attribute `dir="ltr"`. The function then iterates over the
    extracted text to find the required data.
    :return: The `get_name_username` function is returning a tuple containing the name and username
    extracted from the article. The name is stored at index 0 of the `main_post` list, and the username
    is stored at index 1.
    """

    handle_list = article.xpath('.//div[@dir="ltr"]//span/text()').extract()
    main_post = []
    for handle in handle_list:
        if handle == "·":
            break
        main_post.append(handle)
    return main_post[0],''

def get_content(article):
    """
    The function `get_content` extracts text content, hashtags, and mentions from a given article using
    XPath.
    
    :param article: The `article` parameter seems to be a reference to an HTML element that contains
    tweet text content. The `get_content` function is designed to extract the text content from this
    HTML element and then parse it to find mentions (text starting with '@') and hashtags (text starting
    with '#').  `
    :return: The `get_content` function is returning a tuple containing the joined content of the
    article, a list of hashtags found in the content, and a list of mentions found in the content.
    """
    def parse_content(content):
        mentions = []
        hashtags = []
        for txt in content:
            if txt.startswith('@'):
                mentions.append(txt)
            elif txt.startswith('#'):
                hashtags.append(txt)
        return " ".join(content), hashtags, mentions
    content = article.xpath('.//div[@data-testid="tweetText"]//text()').extract()
    return parse_content(content)

def get_reply(article):
    return article.xpath('.//div[@data-testid="reply"]//span/text()').get()
def get_retweets(article):
    return article.xpath('.//div[@data-testid="retweet"]//span/text()').get()
def get_likes(article):
    return article.xpath('.//div[@data-testid="like"]//span/text()').get()
def get_bookmark(article):
    return article.xpath('.//div[@data-testid="bookmark"]//span/text()').get()
def get_tweet_time(article):
    return article.xpath('.//time/@datetime').get()
def get_tweet_id(article):
    return article.xpath('.//time/../@href').get().split('/')[-1]
def get_tweet_handle(article):
    return article.xpath('.//time/../@href').get().split('/')[-3]
def get_tweet_url(article):
    return article.xpath('.//time/../@href').get()

def get_tweet_data(org_tweet_id, url, main_element, start_date = None, end_date = None, ignore_date = True):
    """
    The function `get_tweet_data` extracts various data elements from a tweet based on specified
    criteria such as date range and original tweet ID.
    """
    date = get_tweet_time(main_element)
    is_retweet = False
    retweet_link = None
    pinned_post = False
    if main_element.xpath('.//div[@class="css-175oi2r"]//div[@data-testid="socialContext"]/span[text()="Pinned"]').get():
        pinned_post = True
    if main_element.xpath('.//div[@class="css-175oi2r"]//span[@data-testid="socialContext"]').get():
        print('Is a retweet')
        is_retweet = True
        url = None
        retweet_link = get_tweet_url(main_element)
    datetime_object = datetime.fromisoformat(date.replace('Z', '+00:00'))
    if not ignore_date:
        if datetime_object <= start_date and is_retweet is False and pinned_post is False:
            print(f"Extraction complete as the tweet {datetime_object} falls before", f"{start_date}, {end_date}")
            return None
        if end_date <= datetime_object or datetime_object<=start_date:
            print(f"The TWEET is IGNORED. as the tweet date {datetime_object}, does not fall between the given dates: {start_date} - {end_date}")
            return False
    name, username = get_name_username(main_element)
    content, hashtags, mentions = get_content(main_element)

    reply = get_reply(main_element)
    retweets = get_retweets(main_element)
    likes = get_likes(main_element)
    tweet_id = get_tweet_id(main_element)
    profile_picture = main_element.xpath('.//a[@href="/{twitter_han}"]//img/@src'.format(twitter_han=get_tweet_handle(main_element))).get()
    videos = list(set(main_element.xpath('.//video/source/@src').extract()))
    images = list(set(main_element.xpath('.//div[@class="css-175oi2r"][2]//img/@src').extract()))
    images_2 = list(set(main_element.xpath('.//div[@data-testid="tweetText"]//img/@src').extract()))
    images.extend(images_2)
    links = list(set([link for link in main_element.xpath('.//div[@class="css-175oi2r"][2]//a/@href').extract() if '/status/' not in link]))
    links_2 = list(set([link for link in main_element.xpath('.//div[@data-testid="tweetText"]//a/@href').extract() if 'https:/' in link or 'http:/' in link]))
    links.extend(links_2)
    if org_tweet_id!=tweet_id and ignore_date:
        print(f"Tweet id not matched: {org_tweet_id} <> {tweet_id}")
        return False
    if not retweet_link:
        url = get_tweet_url(main_element)
    return {
        'tweet_id':"'"+tweet_id,
        'username':get_tweet_handle(main_element),
        'name':name,
        'profile_picture':profile_picture,
        'replies':reply,
        'retweets':retweets,
        'likes':likes,
        'is_retweet':is_retweet,
        'retweet_link':retweet_link,
        'posted_time':date.replace('Z', '+00:00'),
        'content':content,
        'hashtags':hashtags,
        'mentions':mentions,
        'images':list(set(images)),
        'videos':videos,
        'tweet_url':url,
        'link':list(set(links))
    }

def get_tweet_reply(url, main_element):
    """
    This Python function extracts various details from a tweet element on a webpage and returns them in
    a structured format.
    """
    date = get_tweet_time(main_element)
    name, username = get_name_username(main_element)
    content, hashtags, mentions = get_content(main_element)
    reply = get_reply(main_element)
    retweets = get_retweets(main_element)
    likes = get_likes(main_element)
    tweet_id = get_tweet_id(main_element)
    profile_picture = main_element.xpath('.//a[@href="/{twitter_han}"]//img/@src'.format(twitter_han=get_tweet_handle(main_element))).get()
    videos = list(set(main_element.xpath('.//video/source/@src').extract()))
    images = list(set(main_element.xpath('.//div[@class="css-175oi2r"][2]//img/@src').extract()))
    images_2 = list(set(main_element.xpath('.//div[@data-testid="tweetText"]//img/@src').extract()))
    images.extend(images_2)
    links = list(set([link for link in main_element.xpath('.//div[@class="css-175oi2r"][2]//a/@href').extract() if '/status/' not in link]))
    links_2 = list(set([link for link in main_element.xpath('.//div[@data-testid="tweetText"]//a/@href').extract() if 'https:/' in link or 'http:/' in link]))
    links.extend(links_2)
    is_retweet = False
    retweet_link = None
    if main_element.xpath('.//div[@class="css-175oi2r"]//span[@data-testid="socialContext"]').get():
        is_retweet = True
        url = None
        retweet_link = get_tweet_url(main_element)
    if not retweet_link:
        url = get_tweet_url(main_element)
    return {
        'tweet_id':"'"+tweet_id,
        'username': get_tweet_handle(main_element),
        'name':name,
        'profile_picture':profile_picture,
        'replies':reply,
        'retweets':retweets,
        'likes':likes,
        'is_retweet':is_retweet,
        'retweet_link':retweet_link,
        'posted_time':date.replace('Z', '+00:00'),
        'content':content,
        'hashtags':hashtags,
        'mentions':mentions,
        'images':list(set(images)),
        'videos':videos,
        'tweet_url':url,
        'link':list(set(links))
    }

def extract_profile(driver, handle_name, start_date, end_date, profile_tweets_file):
    """
    This Python function extracts and saves profile tweets from a specified Twitter handle within a
    given date range.
    """
    handle_link = "https://twitter.com/{twitter_handle}".format(twitter_handle=handle_name)
    driver.get(handle_link)
    sleep(8)
    already_checked = {}
    inital_check = True
    while True:
        elements = driver.find_elements(by.XPATH,'//article[@data-testid="tweet"]')
        starting_count = len(elements)
        if inital_check==True and starting_count==0:
            print(f'No Tweets found for given handle name: {handle_name}')
            break
        print(starting_count)
        for itr in range(len(elements)):
            try:
                temp_tweet_id = elements[itr].find_element(by.XPATH,'.//a[contains(@href,"/status/")]').get_attribute('href')
                temp_tweet_id = extract_tweet_id(temp_tweet_id)
            except:
                break
            if already_checked.get(temp_tweet_id) is None:
                already_checked[temp_tweet_id] = True
            else:
                if itr==len(elements)-1:
                    driver.execute_script("return arguments[0].scrollIntoView(true);", elements[itr])
                sleep(1)
                continue
            if '\nAd\n' in elements[itr].text:
                continue
            driver.execute_script("return arguments[0].scrollIntoView(true);", elements[itr])

            respones = Selector(text=elements[itr].get_attribute("outerHTML"))
            main_element = respones.xpath('//article[@data-testid="tweet"]')[0]
            tweet = get_tweet_data("",driver.current_url,main_element, start_date, end_date, False)
            print(tweet)
            if tweet is None:
                return
            if tweet is not False:
                save_to_csv(tweet,profile_tweets_file)
            sleep(1)

def extract_reply(driver, tweet_id, reply_tweets_file):
    """
    This Python function extracts replies to a specific tweet on Twitter using a web driver and saves
    them to a CSV file.
    """
    tweet_link = "https://twitter.com/i/web/status/{tweet_id}".format(tweet_id=tweet_id)
    driver.get(tweet_link)
    sleep(10)
    already_checked = {}
    main_post = True
    check_counter = 0
    while True:
        if check_counter >= 35:
            break
        # elements = driver.find_elements(by.XPATH,'//article[@data-testid="tweet"]')
        elements = driver.find_elements(
            by.XPATH,
            '//article[@data-testid="tweet"]|//div[@data-testid="cellInnerDiv"]//span[text()="Discover more"]|//div[@data-testid="cellInnerDiv"]//span[text()="Show more replies"]|//div[@data-testid="cellInnerDiv"]//span[text()="Show"]'
            )
        starting_count = len(elements)
        print(starting_count)
        for itr in range(len(elements)):
            if elements[itr].text == 'Show more replies':
                elements[itr].click()
                sleep(10)
                break
            if elements[itr].text == 'Show':
                elements[itr].click()
                sleep(10)
                break
            if elements[itr].text == 'Discover more':
                check_counter = 35
                break
            try:
                temp_tweet_id = elements[itr].find_element(by.XPATH,'.//a[contains(@href,"/status/")]').get_attribute('href')
                temp_tweet_id = extract_tweet_id(temp_tweet_id)
            except Exception as ex:
                break
            if main_post:
                if temp_tweet_id == tweet_id:
                    main_post = False
                already_checked[temp_tweet_id] = True
                continue
            if already_checked.get(temp_tweet_id) is None:
                already_checked[temp_tweet_id] = True
            else:
                check_counter +=1
                if itr==len(elements)-1:
                    driver.execute_script("return arguments[0].scrollIntoView(true);", elements[itr])
                # print("check_counter: ",check_counter)
                sleep(1)
                continue
            if '\nAd\n' in elements[itr].text:
                continue
            driver.execute_script("return arguments[0].scrollIntoView(true);", elements[itr])
            check_counter = 0
            respones = Selector(text=elements[itr].get_attribute("outerHTML"))
            main_element = respones.xpath('//article[@data-testid="tweet"]')[0]
            tweet = get_tweet_reply(driver.current_url,main_element)
            print(tweet)
            save_to_csv(tweet,reply_tweets_file)
            sleep(1)

def read_bulk_tweet_ids_frm_csv(file_name):
    tweet_ids = [str(tweet.strip()) for tweet in open(file_name,'r',encoding='utf-8').readlines() if str(tweet.strip()) != '']
    return tweet_ids

def read_bulk_handles(file_name):
    df = pd.read_csv(file_name)
    final = [
        [handle_name, datetime.fromisoformat(start_date), datetime.fromisoformat(end_date)]
        for handle_name, start_date, end_date in zip(df['handle_name'], df['start_date'], df['end_date'])
    ]
    return final

TWEET_LINK = "https://twitter.com/i/web/status/{tweet_id}"

# Default values
method = None
file_name = None
BULK_TWEET_FILE_NAME = None
BULK_HANDLE_FILE_NAME = None
TWITTER_HANDLE_NAME = None
SEARCH_TWEET_ID = None
START_DATE = None
END_DATE = None
# Parse command line arguments
for arg in sys.argv[1:]:
    key, value = arg.split('=')
    if key == 'method':
        method = int(value)
    elif key == 'tweetIDbatch':
        BULK_TWEET_FILE_NAME = value
    elif key == 'handlenamebatch':
        BULK_HANDLE_FILE_NAME = value
    elif key == 'save_file':
        file_name = value
    elif key == 'handlename':
        TWITTER_HANDLE_NAME = value
    elif key == 'tweetID':
        SEARCH_TWEET_ID = value
    elif key == 'startdate':
        START_DATE = datetime.fromisoformat(value)
    elif key == 'enddate':
        END_DATE = datetime.fromisoformat(value)

# Validate arguments
if method is None:
    print("Error: No method provided. Exiting...")
    sys.exit(1)

driver = get_driver_chrome()
# input('Here')
login(driver)

def method_one(driver, tweet_id, file_name):
    driver.get(TWEET_LINK.format(tweet_id=tweet_id))
    sleep(20)
    respones = Selector(text=driver.page_source)
    main_elements = respones.xpath('//article[@data-testid="tweet"]')
    for main_element in main_elements:
        tweet = get_tweet_data(str(tweet_id),driver.current_url,main_element)
        print(tweet)
        if tweet:
            save_to_csv(tweet,file_name)
            break


extraction_type = method
if extraction_type == 1:
    # For extracting only given tweets.
    if file_name is None or not file_name.endswith('.csv'):
        print("Error: Save file should be in csv format. Exiting...")
        driver.close()
        sys.exit(1)
    if BULK_TWEET_FILE_NAME:
        if not BULK_TWEET_FILE_NAME.endswith('.txt'):
            print("Error: Input file should be in txt format. Exiting...")
            driver.close()
            sys.exit(1)
        tweet_to_scrape = read_bulk_tweet_ids_frm_csv(BULK_TWEET_FILE_NAME)
        for tweet in tweet_to_scrape:
            method_one(driver,tweet, file_name)

    elif SEARCH_TWEET_ID:
        method_one(driver, SEARCH_TWEET_ID, file_name)
    
    else:
        print('Input commands not entered correctly. Please refer to the README.md file for command references. Exiting...')

elif extraction_type == 2:
    # For extracting given tweets from given twitter handle, between `start_date` and `end_date`
    print('Records are saved for each handle in seperate file')
    if BULK_HANDLE_FILE_NAME:
        if not BULK_HANDLE_FILE_NAME.endswith('.csv'):
            print("Error: Input file should be in csv format. Exiting...")
            driver.close()
            sys.exit(1)

        twitter_accounts = read_bulk_handles(BULK_HANDLE_FILE_NAME)
        for twitter_handle, start_date, end_date in twitter_accounts:
            if end_date < start_date:
                print('Error: Start date should be less then end date')
            print(f"Starting extraction of {twitter_handle}'s Tweets between dates from {str(start_date)} to {str(end_date)}")
            profile_tweets_file = f"{twitter_handle}_{str(start_date).split('+')[0].replace(':','_').replace(' ','_')}___{str(end_date).split('+')[0].replace(':','_').replace(' ','_')}.csv"
            extract_profile(driver, twitter_handle, start_date, end_date, profile_tweets_file)
    elif TWITTER_HANDLE_NAME and START_DATE and END_DATE:
        if END_DATE < START_DATE:
            print('Error: start_date should be less than end_date. Exiting...')
            driver.close()
            sys.exit(1)
        print(f"Starting extraction of {TWITTER_HANDLE_NAME}'s Tweets between dates from {str(START_DATE)} to {str(END_DATE)}")
        profile_tweets_file = f"{TWITTER_HANDLE_NAME}_{str(START_DATE).split('+')[0].replace(':','_').replace(' ','_')}___{str(END_DATE).split('+')[0].replace(':','_').replace(' ','_')}.csv"
        extract_profile(driver, TWITTER_HANDLE_NAME, START_DATE, END_DATE, profile_tweets_file)
elif extraction_type == 3:
    print('Records are saved for each handle in seperate file')

    if BULK_TWEET_FILE_NAME:
        if not BULK_TWEET_FILE_NAME.endswith('.txt'):
            print("Error: Input file should be in txt format. Exiting...")
            driver.close()
            sys.exit(1)
        tweet_to_scrape = read_bulk_tweet_ids_frm_csv(BULK_TWEET_FILE_NAME)
        for tweet in tweet_to_scrape:
            print(f"Starting Tweet extraction for tweet: {tweet}")
            file_name = f'{tweet}.csv'
            extract_reply(driver, tweet, file_name)
    elif SEARCH_TWEET_ID:
        file_name = f'{SEARCH_TWEET_ID}.csv'
        extract_reply(driver, SEARCH_TWEET_ID, file_name)

driver.close()