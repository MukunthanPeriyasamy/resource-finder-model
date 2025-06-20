from langchain_community.utilities import SerpAPIWrapper
from googleapiclient.discovery import build
import os
from fastapi import FastAPI  # update this path to match your project

app = FastAPI()

@app.get("/search")
def search(query: str):
    return find_resources(query)

# Set your SerpAPI key
os.environ["SERPAPI_API_KEY"] = "8cafaef62871efcbd48c090e1caa36caa5e9f68db7e44be1b427ca33b099ffcf"
# === YouTube Search ===
YOUTUBE_API_KEY = "AIzaSyCIs3T_i2DbUK6fYT04gZ51e6SIw1XmUMY"

# Initialize YouTube API client
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# === Web Search using SerpAPI ===
def search_web_links(query, max_results):
    search = SerpAPIWrapper()
    results = search.results(query)

    web_links = []
    for item in results.get("organic_results", [])[:max_results]:
        title = item.get("title")
        url = item.get("link")
        snippet = item.get("snippet", "")
        if title and url:
            web_links.append({
                "source": "web",
                "title": title,
                "url": url,
                "snippet": snippet
            })
    return web_links


def search_youtube_links(query, max_results):
    request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=max_results
    )
    response = request.execute()

    video_links = []
    for item in response.get('items', []):
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        link = f"https://www.youtube.com/watch?v={video_id}"
        video_links.append({
            "source": "youtube",
            "title": title,
            "url": link,
            "snippet": ""
        })
    if not video_links:
        return "nothing found"
    return video_links


# === Combined Resource Finder ===
def find_resources(query, max_results=3):
    web_results = search_web_links(query, max_results)
    youtube_results = search_youtube_links(query, max_results)
    return {"web": web_results, "youtube": youtube_results}


# === Test Example ===
query = input("Search for the resource:\n")
resources = find_resources(query)

# Print Web Articles
print("\n📚 ARTICLE LINKS:\n")
for i, item in enumerate(resources['web'], 1):
    print(f"{i}. {item['title']}\n   {item['url']}")
    print()

# Print YouTube Videos
print("\n🎥 YOUTUBE LINKS:\n")
for i, item in enumerate(resources['youtube'], 1):
    print(f"{i}. {item['title']}\n   {item['url']}")
    print()

