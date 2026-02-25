from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Literal
import random


class AgentState(TypedDict):
    player_name: str
    number: int              
    attempts: int
    lower_bound: int
    upper_bound: int
    guess: int
    status: str              


def setup(state: AgentState) -> AgentState:
    if "lower_bound" not in state:
        state["lower_bound"] = 1
    if "upper_bound" not in state:
        state["upper_bound"] = 20

    state["player_name"] = f"Hi there, {state['player_name']}"
    state["number"] = random.randint(state["lower_bound"], state["upper_bound"])
    state["attempts"] = 0
    state["status"] = ""
    state["guess"] = 0
    return state


def guesser(state: AgentState) -> AgentState:
    lo = state["lower_bound"]
    hi = state["upper_bound"]

    if lo > hi:
        lo, hi = hi, lo

    state["guess"] = (lo + hi) // 2
    return state


def hint(state: AgentState) -> AgentState:
    state["attempts"] += 1

    if state["guess"] < state["number"]:
        state["status"] = "Higher"
    elif state["guess"] > state["number"]:
        state["status"] = "Lower"
    else:
        state["status"] = "Correct"

    print(f"Attempt {state['attempts']}: guess={state['guess']} -> {state['status']}")
    return state


def update_bounds(state: AgentState) -> AgentState:
    # Use the hint to shrink the search space
    if state["status"] == "Higher":
        state["lower_bound"] = state["guess"] + 1
    elif state["status"] == "Lower":
        state["upper_bound"] = state["guess"] - 1
    # If Correct: do nothing
    return state


def decider(state: AgentState) -> Literal["loop", "exit"]:
    # Exit if correct OR attempts exhausted
    if state["status"] == "Correct" or state["attempts"] >= 7:
        return "exit"
    return "loop"


# Build graph
graph = StateGraph(AgentState)

graph.add_node("setup", setup)
graph.add_node("guesser", guesser)
graph.add_node("hint", hint)
graph.add_node("update_bounds", update_bounds)

graph.add_edge(START, "setup")
graph.add_edge("setup", "guesser")
graph.add_edge("guesser", "hint")
graph.add_edge("hint", "update_bounds")

graph.add_conditional_edges(
    "update_bounds",
    decider,
    {
        "loop": "guesser",
        "exit": END,
    }
)

app = graph.compile()

# Run
result = app.invoke({
    "player_name": "Tan",
    "lower_bound": 1,
    "upper_bound": 20,
    # the rest will be filled in setup
})
print("\nFINAL STATE:", result)


graph= StateGraph(AgentState)
graph.add_node("first_node", setup)
graph.add_node("second_node", hint)



