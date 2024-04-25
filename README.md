# Twitter Scraping Bot
The Twitter Scraping Bot is a tool designed for extracting various data points from tweets, including tweet metadata, content, and media.

## Requirments
Ensure that Python is installed on your system. You can download Python from here, and the version should be >=3.11.0.
After installing Python, open your terminal and navigate to the project directory. Then, install the required packages by running the following command:
```bash
pip install -r requirements.txt
```

Before using the Twitter Scraping Bot, make sure to set up your Twitter credentials in the credentials.py file.
```bash
my_user_email = "YOUR USERNAME/EMAIL"
my_password = "YOUR PASSWORD"
my_user_handle = "YOUR HANDLE NAME"
my_registered_number = "YOUR REGISTERED NUMBER"
```

## Usage
Run the script `twitter_selenium.py` with appropriate command-line arguments to specify the extraction method and other parameters. The available extraction methods are as follows:

### Method 1: Extracting Main Tweets
This method extracts the main tweet based on the provided tweet IDs. It requires a txt file containing tweet IDs.
Commands:
- To run in batch mode:
```bash
python twitter_selenium.py method=1 tweetIDbatch=<file_path> save_file=<output_file.csv>
```
To run in single mode:
```bash
python twitter_selenium.py method=1 tweetID=<tweet_ID> save_file=<output_file.csv>
```
Examples:
- To run in batch mode example:
```bash
python twitter_selenium.py method=1 tweetIDbatch=bulk_tweets.txt save_file=tweets_method_1_batch.csv
```
- To run in sigle mode example:

```bash
python twitter_selenium.py method=1 tweetID=1739330160766402630 save_file=tweets_methods_1_single.csv
```
### Method 2: Extracting Tweets from a Profile
This method extracts tweets from a specified Twitter profile between the given start and end dates. It requires a CSV file containing Twitter handles, start dates, and end dates.
Commands:
- To run in batch mode:
```bash
python twitter_selenium.py method=2 handlenamebatch=<file_path>
```
- To run in single mode:
```bash
python twitter_selenium.py method=2 handlename=<handle_name> startdate=<start_date> enddate=<end_date>

```
Example:
- To run in single mode example:
```bash
python twitter_selenium.py method=2 handlenamebatch=bulk_handle.csv
```
- To run in batch mode example:
```bash
python twitter_selenium.py method=2 handlename=tim_cook enddate=2024-02-05T15:32:43+00:00 startdate=2024-01-01T15:32:43+00:00
```
- Note that the format of the date is `2024-02-05T15:32:43+00:00`. 
- The startdate should always be smaller than enddate

### Method 3: Extracting Replies from a Tweet
This method extracts replies to a specific tweet. It requires tweet ID.

Command:
- To run in batch mode:
```bash
python twitter_selenium.py method=3 tweetIDbatch=<file_path>
```
- To run in single mode:
```bash
python twitter_selenium.py method=3 tweetID=<tweet_id>
```
Example:
- To run in batch mode example:
```bash
python twitter_selenium.py method=3 tweetIDbatch=bulk_tweet_reply.txt
```
- To run in single mode example:
```bash
python twitter_selenium.py method=3 tweetID=1745996828724847009
```


## Note
- This is to set up the chrome driver in such a way that logging in is not required.
- If you want to use your google profile that already has twitter logged in. Then open the twitter_selenium script and update the following path with your own path:
- `options.add_argument(r'user-data-dir=C:\Users\Mubashir Ali\AppData\Local\Google\Chrome\User Data')`
- Add the profile number in which the twitter account is logged in.
- `options.add_argument(r'profile-directory=Profile 3')`
- You can check your path by adding the follwing command in chrome address bar:
```bash
chrome://version/
```
- You can find the profile path. Copy it and paste it as described above in the code.
- The line number for these are 26 and 27.
- Additionaly comment the `login(driver)` function call on line 417.
- Also disable any ad blockers that are running on the profile that is meant to be used.