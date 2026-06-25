"""Tavily web search tool for LangGraph."""

import os

from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()


@tool
def web_search(query: str) -> str:
    """Search the web and return top result summaries."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "Search unavailable: TAVILY_API_KEY is not set in .env."
    try:
        from tavily import TavilyClient

        client = TavilyClient(api_key=api_key)
        res = client.search(query, max_results=3, include_answer=True)
        answer = res.get("answer") or ""
        results = "\n".join(
            f"- {r['title']}: {r['url']}" for r in res.get("results", [])[:3]
        )
        return f"{answer}\n{results}".strip()
    except Exception as e:
        return f"Search error: {e}"
