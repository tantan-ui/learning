from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Dict, List
import random

class AgentState(TypedDict):
    name: str
    number: List[int]
    counter:int

def greet_node(state:AgentState)->AgentState:
    """This is the first node"""
    state['name']= f"Hi there, {state['name']}"
    state['counter']= 0
    return state

def random_node(state:AgentState) -> AgentState:
    """This is the random node"""
    state['number'].append(random.randint(1,10))
    state['counter']+=1
    return state

def decider(state:AgentState) -> AgentState:
    """This is the node to tell what to do next"""
    if state['counter'] <= 5:
        print("ENTERING LOOP", state['counter'])
        return "loop"
    else:
        return "exit"
    
graph= StateGraph(AgentState)
graph.add_node("greeter", greet_node)
graph.add_node("random", random_node)
graph.add_edge("greeter","random")

graph.add_conditional_edges(
    "random",
    decider,
    {
        "loop":"random",
        "exit": END

    }

)
graph.add_edge(START, "greeter")
app= graph.compile()

result = app.invoke({"name":"Tan", "number": [], "counter": -1})
print(result)
