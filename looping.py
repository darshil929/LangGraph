from langgraph.graph import StateGraph, START, END
import random
from typing import Dict, List, TypedDict

from IPython.display import Image, display

class AgentState(TypedDict):
    name: str
    number: List[int]
    counter: int
    
def greeting_node(state: AgentState) -> AgentState:
    """Greeting node that says Hi to the person"""
    
    state['name'] = f"Hi there, {state['name']}"
    state['counter'] = 0
    
    return state

def random_node(state: AgentState) -> AgentState:
    """Generates a random number from 0 to 10"""
    
    state['number'].append(random.randint(0, 10))
    state['counter'] += 1
    
    return state

def should_continue(state: AgentState) -> AgentState:
    """This nodes decides what to do next"""
    
    if state['counter'] < 5:
        print("ENTERING LOOP", state['counter'])
        return "loop" # continue looping
    else:
        return "exit" # exit looping
    
graph = StateGraph(AgentState)

graph.add_node("greeting", greeting_node)
graph.add_node("random", random_node)
graph.add_edge("greeting", "random")

graph.add_conditional_edges(
    "random",
    should_continue,
    {
        "loop": "random",
        "exit": END
    }
)

graph.set_entry_point("greeting")

app = graph.compile()

display(Image(app.get_graph().draw_mermaid_png()))

app.invoke({"name": "Darshil", "number": [], "counter": -100})