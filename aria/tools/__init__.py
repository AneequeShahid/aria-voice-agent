"""Tool registry: web search + file ops for LangGraph brain."""

from aria.tools.files import read_file, write_file
from aria.tools.search import web_search

TOOLS = [web_search, read_file, write_file]
