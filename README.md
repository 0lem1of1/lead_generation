Reddit Keyword Monitor with BERT Sentiment Analysis
This project is a powerful, real-time social listening bot that monitors Reddit for specific keywords, performs high-accuracy sentiment analysis using a state-of-the-art BERT model, and sends instant alerts to a Slack channel.

It's designed to be a lightweight, serverless-style script that can be run continuously to keep you informed about conversations relevant to your brand, product, or interests.

Key Features
Real-time Monitoring: Listens to a live stream of comments from multiple subreddits simultaneously.

High-Accuracy Sentiment Analysis: Uses a pre-trained BERT model (DistilBERT) from Hugging Face for nuanced and context-aware sentiment analysis (Positive/Negative).

Instant Slack Alerts: Delivers well-formatted, detailed notifications directly to your Slack workspace for immediate review.

Easy Configuration: All settings, including API keys, keywords, and target subreddits, are managed in simple configuration files or variables.

No Database Required: Operates as a pure real-time alerting tool, making it simple and dependency-free.

How It Works
The bot operates in a continuous four-step cycle:

Listen : Connects to the Reddit API and monitors a live stream of new comments across a list of specified subreddits.

Detect : Scans the text of each comment to see if it contains any of your predefined keywords.

Analyze : If a match is found, the comment's text is sent to the loaded BERT model, which returns a sentiment (Positive/Negative) and a confidence score.

Alert : Formats the keyword, comment details, author, and sentiment analysis into a message and sends it to your designated Slack channel.

Example Slack Alert
Here is an example of what the notification looks like in Slack:

New Reddit Mention (BERT Analysis)!

Keyword: story
Subreddit: r/AskReddit
Author: SomeUser123
Sentiment: Positive (Confidence: 99.87%)

It's a long story, but the short version is that everything worked out wonderfully in the end. It really restored my faith in people.

Link to comment: https://www.google.com/search?q=https://reddit.com/r/AskReddit/comments/...

Setup and Installation
Follow these steps to get your Reddit Monitor Bot running.

1. Prerequisites
Python 3.9+

A Reddit account with API credentials.

A Slack workspace where you can create an App and get a Bot Token.

2. Clone the Repository
Clone this project to your local machine:

git clone <your-repository-url>
cd <repository-directory>

3. Set Up a Virtual Environment
It's highly recommended to use a virtual environment to manage dependencies.

# Create the environment
python -m venv venv

# Activate it
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

4. Install Dependencies
Install all the required Python libraries using the requirements.txt file.

pip install -r requirements.txt

Note: This will download PyTorch and the transformers library, which can be over 1 GB in size.

5. Configure Environment Variables
The script uses a .env file to securely manage API keys and secrets. Create a file named .env in the root of the project directory and add the following content:

# --- Reddit API Credentials ---
REDDIT_CLIENT_ID="your_reddit_client_id"
REDDIT_CLIENT_SECRET="your_reddit_client_secret"
REDDIT_USER_AGENT="AppName v1.0 by u/YourUsername"
REDDIT_USERNAME="your_reddit_username"
REDDIT_PASSWORD="your_reddit_password"

# --- Slack API Credentials ---
SLACK_CHANNEL="#your-alerts-channel-name"
SLACK_BOT_TOKEN="xoxb-your-long-slack-bot-token"

Usage
Once the setup is complete, you can start the bot with a single command.

1. Customize Your Search
Before running, open the reddit_bert_monitor.py script and edit these two lists to match your needs:

# Keywords and subreddits to monitor
KEYWORDS = ["your", "list", "of", "keywords"]
SUBREDDITS_TO_MONITOR = ["AskReddit", "technology", "python"]

2. Run the Bot
Execute the main script from your terminal:

python reddit_bert_monitor.py

The first time you run the script, it will download the BERT model from Hugging Face. This might take a few minutes depending on your internet connection. Subsequent runs will use the cached local version.

The bot will then start listening for comments. You can stop it at any time by pressing CTRL+C.

License
This project is licensed under the MIT License. See the LICENSE file for details.