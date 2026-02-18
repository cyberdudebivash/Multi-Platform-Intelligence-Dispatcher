import requests

# CONFIGURATION
FB_PAGE_ID = "YOUR_FACEBOOK_PAGE_ID"
IG_USER_ID = "YOUR_INSTAGRAM_BUSINESS_ID"
ACCESS_TOKEN = "YOUR_LONG_LIVED_ACCESS_TOKEN"

def post_to_meta(title, url):
    """Post to both Facebook Page and Instagram Business Feed"""
    
    # 1. POST TO FACEBOOK PAGE
    fb_url = f"https://graph.facebook.com/v20.0/{FB_PAGE_ID}/feed"
    fb_payload = {
        'message': f"🚨 [SENTINEL APEX INTEL] {title}\nFull analysis: {url}",
        'link': url,
        'access_token': ACCESS_TOKEN
    }
    fb_res = requests.post(fb_url, data=fb_payload)
    print(f"Facebook: {fb_res.status_code}")

    # 2. POST TO INSTAGRAM (Images/Video only)
    # Note: Instagram requires an image URL; it doesn't support text-only links.
    # We first create a media container, then publish it.
    image_url = "https://your-server.com/cyber_beast_image.jpg" # Must be public
    
    # Create Media Container
    ig_container_url = f"https://graph.facebook.com/v20.0/{IG_USER_ID}/media"
    ig_payload = {
        'image_url': image_url,
        'caption': f"🚨 {title}\n{url} #CyberSecurity #ThreatIntel",
        'access_token': ACCESS_TOKEN
    }
    container_res = requests.post(ig_container_url, data=ig_payload).json()
    
    if 'id' in container_res:
        creation_id = container_res['id']
        # Publish Media Container
        publish_url = f"https://graph.facebook.com/v20.0/{IG_USER_ID}/media_publish"
        publish_res = requests.post(publish_url, data={
            'creation_id': creation_id,
            'access_token': ACCESS_TOKEN
        })
        print(f"Instagram: {publish_res.status_code}")
