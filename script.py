import os
import praw
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from transformers import pipeline, logging as hf_logging


hf_logging.set_verbosity_error()

load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

KEYWORDS = ["question", "people", "think", "what", "like", "would", "story", "time", "life", "secret"]
SUBREDDITS_TO_MONITOR = ["AskReddit", "funny", "gaming", "worldnews", "memes"]



reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD,
)



slack_client = WebClient(token=SLACK_BOT_TOKEN)


print("Loading BERT sentiment analysis model...")
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)
print("BERT model loaded successfully.")



def process_and_alert(comment, keyword_found):
    """
    Analyzes a comment's sentiment using a BERT model and sends a detailed
    alert to a Slack channel.
    """
    print(f"Analyzing comment {comment.id} for sentiment...")

    truncated_comment_body = comment.body[:512]

    analysis_result = sentiment_analyzer(truncated_comment_body)[0]
    sentiment_label = analysis_result['label'].capitalize()  
    sentiment_confidence = analysis_result['score']

    full_permalink = f"https://reddit.com{comment.permalink}"
    author_name = comment.author.name if comment.author else "[deleted]"

    message = (
        f"*New Reddit Mention (BERT Analysis)!*\n\n"
        f"*Keyword:* `{keyword_found}`\n"
        f"*Subreddit:* `r/{comment.subreddit.display_name}`\n"
        f"*Author:* `{author_name}`\n"
        f"*Sentiment:* *{sentiment_label}* `(Confidence: {sentiment_confidence:.2%})`\n\n"
        f"> {comment.body}\n\n"
        f"*Link to comment:* {full_permalink}"
    )

    try:
        slack_client.chat_postMessage(
            channel=SLACK_CHANNEL,
            text=message,
            mrkdwn=True
        )
        print(f"Alert for comment {comment.id} sent to Slack.")
    except SlackApiError as e:
        print(f"Error sending alert to Slack: {e.response['error']}")


def monitor_subreddits():
    """
    Monitors a combined stream of comments from multiple subreddits for specific
    keywords and triggers the processing and alerting function.
    """
    subreddit_names = "+".join(SUBREDDITS_TO_MONITOR)
    subreddit = reddit.subreddit(subreddit_names)

    print(f"Listening for new comments in: r/{subreddit_names}")
    print(f"Keywords: {', '.join(KEYWORDS)}")

    
    for comment in subreddit.stream.comments(skip_existing=True):
        comment_text_lower = comment.body.lower()

        for keyword in KEYWORDS:
            if keyword in comment_text_lower:
                print(f"Match found for '{keyword}' in comment {comment.id}!")
                process_and_alert(comment, keyword)
                break

if __name__ == "__main__":
    required_vars = [
        "REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USER_AGENT",
        "REDDIT_USERNAME", "REDDIT_PASSWORD", "SLACK_CHANNEL", "SLACK_BOT_TOKEN"
    ]
    monitor_subreddits()
