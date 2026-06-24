"""Local file read/write tools for LangGraph."""

import os

from langchain_core.tools import tool


@tool
def read_file(path: str) -> str:
    """Read a local text file relative to the agent working directory."""
    try:
        base = os.path.expanduser("~/aria-workspace")
        full = os.path.abspath(os.path.join(base, path))
        if not full.startswith(base):
            return "Permission denied: path escapes workspace."
        with open(full, "r", encoding="utf-8", errors="replace") as f:
            return f.read()[:4000]
    except FileNotFoundError:
        return f"File not found: {path}"
    except Exception as e:
        return f"Read error: {e}"


@tool
def write_file(path: str, content: str) -> str:
    """Write content to a local text file inside agent workspace."""
    try:
        base = os.path.expanduser("~/aria-workspace")
        os.makedirs(os.path.dirname(os.path.join(base, path)), exist_ok=True)
        full = os.path.abspath(os.path.join(base, path))
        if not full.startswith(base):
            return "Permission denied: path escapes workspace."
        with open(full, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Wrote {len(content)} chars to {path}."
    except Exception as e:
        return f"Write error: {e}"
