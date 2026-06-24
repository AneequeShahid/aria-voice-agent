"""Tavily web search tool for LangGraph."""

from langchain_core.tools import tool

try:
    from tavily import TavilyClient

    _tavily = TavilyClient()
except Exception:
    _tavily = None


@tool
def web_search(query: str) -> str:
    """Search the web and return top result summaries."""
    if _tavily is None:
        return "Search tool unavailable: tavily not initialised."
    try:
        res = _tavily.search(query, max_results=3, include_answer=True)
        answer = res.get("answer") or ""
        results = "\n".join(
            f"- {r['title']}: {r['url']}" for r in res.get("results", [])[:3]
        )
        return f"{answer}\n{results}".strip()
    except Exception as e:
        return f"Search error: {e}"
