import feedparser
import tweepy
import requests
import json
from mastodon import Mastodon
from atproto import Client
from datetime import datetime, timezone

# --- CONFIGURATION: REPLACING CREDENTIALS ---
# RSS Source for CYBERDUDEBIVASH Intel
RSS_URL = "https://cyberbivash.blogspot.com/feeds/posts/default?alt=rss"

# X (Twitter) Credentials
X_CREDS = {
    "api_key": "YOUR_X_API_KEY",
    "api_secret": "YOUR_X_API_SECRET",
    "access_token": "YOUR_X_ACCESS_TOKEN",
    "access_secret": "YOUR_X_ACCESS_SECRET"
}

# LinkedIn Company Page Details
LI_ACCESS_TOKEN = "YOUR_LINKEDIN_PAGE_ACCESS_TOKEN"
LI_ORG_ID = "YOUR_LINKEDIN_COMPANY_NUMERIC_ID" # e.g. 61583373732736

# --- PLATFORM DISPATCH FUNCTIONS ---

def post_to_x(message):
    """Post tactical alert to @cyberbivash"""
    client = tweepy.Client(
        consumer_key=X_CREDS["api_key"], consumer_secret=X_CREDS["api_secret"],
        access_token=X_CREDS["access_token"], access_token_secret=X_CREDS["access_secret"]
    )
    client.create_tweet(text=message)

def post_to_linkedin(title, url):
    """Post to CyberDudeBivash Pvt Ltd via Posts API"""
    api_url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {LI_ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    post_data = {
        "author": f"urn:li:organization:{LI_ORG_ID}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": f"[CDB Sentinel Intel] 🚨 {title}"},
                "shareMediaCategory": "ARTICLE",
                "media": [{"status": "READY", "originalUrl": url}]
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }
    requests.post(api_url, headers=headers, json=post_data)

def post_to_mastodon(message):
    """Dispatch to @cyberdudebivash on Mastodon"""
    m = Mastodon(access_token='YOUR_MASTODON_TOKEN', api_base_url='https://mastodon.social')
    m.toot(message)

def post_to_bluesky(message):
    """Post to Bluesky via AT Protocol"""
    client = Client()
    client.login('cyberdudebivash.bsky.social', 'YOUR_APP_PASSWORD')
    client.send_post(message)

# --- MAIN AUTOMATION ENGINE ---

def run_dispatcher():
    feed = feedparser.parse(RSS_URL)
    if not feed.entries: return
    
    latest = feed.entries[0]
    title = latest.title
    link = latest.link
    
    # Unified tactical format for high impact
    tactical_msg = f"🚨 [SENTINEL APEX INTEL] {title}\nFull technical dossier: {link}\n#CyberSecurity #ThreatIntel #CDB_Sentinel"
    
    # Broadcast to all spokes
    try: post_to_x(tactical_msg)
    except Exception as e: print(f"X Post Failed: {e}")
    
    try: post_to_linkedin(title, link)
    except Exception as e: print(f"LinkedIn Failed: {e}")
    
    try: post_to_mastodon(tactical_msg)
    except Exception as e: print(f"Mastodon Failed: {e}")

if __name__ == "__main__":
    run_dispatcher()
