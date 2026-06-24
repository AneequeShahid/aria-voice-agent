"""LangGraph brain: Groq LLM agent with tool calling and ChromaDB memory."""

from typing import Annotated

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from typing_extensions import TypedDict

from aria.memory import search_memory, add_memory
from aria.tools import TOOLS

MODEL = "llama3-8b-8192"


class State(TypedDict):
    messages: list


def build_agent(session_id: str = "default") -> StateGraph:
    llm = ChatGroq(model=MODEL, temperature=0.4, max_tokens=512)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are Aria, a helpful voice assistant. "
                "Be concise — 1-3 sentences. "
                "Use tools when asked for current info, files, or calculations.",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    memory = MemorySaver()

    agent = create_react_agent(
        llm,
        TOOLS,
        state_modifier=prompt,
        checkpointer=memory,
    )

    graph = StateGraph(State)
    graph.add_node("agent", agent)
    graph.set_entry_point("agent")
    graph.add_edge("agent", END)
    return graph.compile(checkpointer=memory)


def run_brain(user_text: str, session_id: str = "default") -> str:
    past = search_memory(session_id, user_text, n=3)
    context = ""
    if past:
        context = "\n".join(f"- {m}" for m in past)

    graph = build_agent(session_id)
    config = {"configurable": {"thread_id": session_id}}
    result = graph.invoke(
        {
            "messages": [
                {"role": "system", "content": f"Recent relevant memory:\n{context}"},
                {"role": "user", "content": user_text},
            ]
        },
        config=config,
    )
    answer = result["messages"][-1].content.strip()
    add_memory(session_id, user_text)
    add_memory(session_id, answer)
    return answer
