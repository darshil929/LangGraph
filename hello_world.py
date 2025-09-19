from typing import Dict, TypedDict
from langgraph.graph import StateGraph # framework that helps us design and manage the flow of tasks in our applications using a graph structure

from IPython.display import Image, display

# We now create an AgentState - shared data structure that keeps track of the information as your application runs

class AgentState(TypedDict): # Our state schema
    message: str
    
def greeting_node(state: AgentState) -> AgentState:
    """Simple node that adds a greeting message to the state""" # adding doc strings in these functions is very important as it lets the LLMs that we use know what the certain function does
    
    state['message'] = "Hey " + state['message'] + "!, how is your day going?"
    
    return state

graph = StateGraph(AgentState)

graph.add_node("greeter", greeting_node)

graph.set_entry_point("greeter")
graph.set_finish_point("greeter")

app = graph.compile()

display(Image(app.get_graph().draw_mermaid_png()))

result = app.invoke({"message": "World"})

print(result["message"])

