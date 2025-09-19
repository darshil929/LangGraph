from typing import TypedDict, List
from langgraph.graph import StateGraph

import math

from IPython.display import Image, display

class AgentState(TypedDict):
    values: List[int]
    name: str
    operation: str
    result: str
    
def process_values(state: AgentState) -> AgentState:
    """This function handles multiple different inputs"""
    
    if state["operation"] == "+":
        state["result"] = f"Hi there {state['name']}! Your sum is equal to {sum(state['values'])}."
    elif state["operation"] == "*":
        state["result"] = f"Hi there {state['name']}! Your product is equal to {math.prod(state['values'])}."
    else:
        state["result"] = f"Hi there {state['name']}! please provide a relevant operation to perform."
        
    return state

graph = StateGraph(AgentState)

graph.add_node("processor", process_values)
graph.set_entry_point("processor")
graph.set_finish_point("processor")

app = graph.compile()

display(Image(app.get_graph().draw_mermaid_png()))

answer1 = app.invoke({"values": [1,2,3,4], "name": "Darshil", "operation": "+"})
answer2 = app.invoke({"values": [1,2,3,4], "name": "Darshil", "operation": "*"})
answer3 = app.invoke({"values": [1,2,3,4], "name": "Darshil", "operation": "/"})

print(answer1["result"])
print(answer2["result"])
print(answer3["result"])

