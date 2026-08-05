import os
import requests 
from dotenv import load_dotenv

def web_search(query, num_results = 5):
    """
    Uses Tavily API to search the web.
    Returns a list of {title, url, snippet}.
    """
    load_dotenv()
    api_key = os.environ.get("API_KEY")
    resp = requests.post(
        "https://api.tavily.com/search",
        json={"api_key": api_key, "query": query, "max_results": num_results}
    )
    resp.raise_for_status()
    data = resp.json()
    results = []
    for each_dict in data.get("results", []):
        results.append({
            "title": each_dict.get("title", ""),
            "url": each_dict.get("url", ""),
            "snippet": each_dict.get("content", "")[:400]
        })
    formatted = "\n\n".join(
    f"{i+1}. Title: {r['title']}\n"
    f"Snippet: {r['snippet']}\n"
    f"URL: {r['url']}"
    for i, r in enumerate(results)
)

    return formatted

