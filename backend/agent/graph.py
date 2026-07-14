from langgraph.graph import StateGraph, END
from .state import AgentState
from .tools import (
    summarize_interaction,
    suggest_followup,
)


def chatbot(state: AgentState):
    text = state["text"]

    if text.startswith("summarize:"):
        response = summarize_interaction.invoke(
            {"text": text.replace("summarize:", "").strip()}
        )

    elif text.startswith("followup:"):
        response = suggest_followup.invoke(
            {"text": text.replace("followup:", "").strip()}
        )

    else:
        response = summarize_interaction.invoke(
            {"text": text}
        )

    return {
        "response": response
    }


builder = StateGraph(AgentState)

builder.add_node("chatbot", chatbot)

builder.set_entry_point("chatbot")
builder.add_edge("chatbot", END)

graph = builder.compile()